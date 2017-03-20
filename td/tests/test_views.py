from __future__ import absolute_import

import importlib
import re
import types
import requests
import json
from absoluteuri import reverse

from mock import patch, Mock

from django.http import HttpResponse, JsonResponse
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.conf import settings

from djcelery.tests.req import RequestFactory

from ..models import TempLanguage, Language
from ..resources.models import Questionnaire
from ..views import TempLanguageListView, TempLanguageDetailView, TempLanguageUpdateView, AjaxTemporaryCode,\
    TempLanguageAdminView, TempLanguageWizardView, LanguageDetailView, codes_text_export, names_text_export,\
    names_json_export, gateway_languages_autocomplete
from ..forms import TempLanguageForm
from ..tests.models import NoSignalTestCase


def setup_view(view, request=None, *args, **kwargs):
    """
    Mimic as_view() by returning the view instance.
    args and kwargs are the same as you would pass to reverse()
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


def create_user():
    """
    """
    return User.objects.create_user(
        username="test_user",
        email="test@gmail.com",
        password="test_password",
    )


class CodesTextExportTestCase(TestCase):

    @patch("td.tracking.models.Language.codes_text")
    def test_return_http(self, mock_codes_text):
        response = codes_text_export(None)

        # Must call Language.codes_text()
        mock_codes_text.assert_called_once_with()

        # Must return HttpResponse
        self.assertIsInstance(response, HttpResponse)


class NamesTextExportTestCase(TestCase):

    @patch("td.tracking.models.Language.names_text")
    def test_return_http(self, mock_names_text):
        response = names_text_export(None)

        # Must call Language.names_text()
        mock_names_text.assert_called_once_with()

        # Must return HttpResponse
        self.assertIsInstance(response, HttpResponse)


class NamesJsonExportTestCase(TestCase):

    @patch("td.models.JSONData.objects.get")
    def test_return_json(self, mock_jsondata_get):
        mock_jsondata_get.return_value.data = ""
        response = names_json_export(None)

        # Must call JSONData.objects.get(name="langnames")
        mock_jsondata_get.assert_called_once_with(name="langnames")

        # Must return JsonResponse
        self.assertIsInstance(response, JsonResponse)


class LanguageDetailViewTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("uw/languages/")
        self.request.user = create_user()
        self.view = setup_view(LanguageDetailView(), self.request)
        self.view.object = Language.objects.create(pk=999, code="tst", name="test")

    @patch("td.views.requests")
    def test_get_context_data(self, mock_requests):
        mock_requests.get.return_value.status_code = 505
        context = self.view.get_context_data()
        self.assertIn("jp_status_code", context)
        self.assertIn("jp", context)
        self.assertIn("language", context)
        self.assertIn("countries", context)
        self.assertIn("country", context)

    @patch("td.views.requests")
    def test_get_context_data_error(self, mock_requests):
        mock_response = requests.Response()
        mock_response._content = "this should throw an error when json tries to decode"
        mock_requests.get.return_value = mock_response
        context = self.view.get_context_data()
        self.assertEqual(context["jp_status_code"], "204")
        self.assertIsNone(context["jp"])


class TempLanguageListViewTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/uw/templanguages/")
        self.request.user = create_user()
        self.view = setup_view(TempLanguageListView(), self.request)

    def test_get_with_user(self):
        """
        Requesting TempLanguage list should return successful response
        """
        response = TempLanguageListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for view config
        """
        self.assertIs(self.view.model, TempLanguage)
        self.assertEqual(self.view.template_name, "resources/templanguage_list.html")


class TempLanguageDetailViewTestCase(NoSignalTestCase):
    def setUp(self):
        super(TempLanguageDetailViewTestCase, self).setUp()
        obj = TempLanguage(pk=999, code="tst")
        obj.save()
        self.request = RequestFactory().get("/uw/templanguages/")
        self.request.user = create_user()
        self.view = setup_view(TempLanguageDetailView(), self.request)

    def test_get_with_user(self):
        """
        Requesting TempLanguage list should return successful response
        """
        response = TempLanguageDetailView.as_view()(self.request, pk=999)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for view config
        """
        self.assertIs(self.view.model, TempLanguage)
        self.assertEqual(self.view.template_name, "resources/templanguage_detail.html")


class TempLanguageWizardViewTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/uw/templanguages/create/")
        self.request.user = create_user()
        self.questionnaire = Questionnaire.objects.create(questions=[
            {"id": 0, "text": "question 1", "help": "", "required": True, "input_type": "string", "depends_on": None},
            {"id": 1, "text": "question 2", "help": "", "required": True, "input_type": "string", "depends_on": 0},
            {"id": 2, "text": "question 3", "help": "", "required": True, "input_type": "string", "depends_on": None}
        ])
        self.view = setup_view(TempLanguageWizardView(), self.request)
        # WizardView will look to use session
        engine = importlib.import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        setattr(self.request, "session", store)

    def test_get_with_user(self):
        """
        Requesting temporary language creation form should return a success response
        """
        response = TempLanguageWizardView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_init(self):
        """
        __init__() should create TempLanguageWizardView.questionnaire
        """
        self.view.__init__()
        self.assertIsInstance(self.view.questionnaire, Questionnaire)
        self.assertEqual(self.view.questionnaire, self.questionnaire)

    @patch("td.views.TempLanguage.save")
    @patch("td.views.redirect")
    def test_done(self, mock_redirect, mock_save):
        """
        done() should save TempLanguage and return a redirect
        """
        mock_cleaned_data = {
            "code": "tst",
            "questionnaire": self.questionnaire,
        }
        self.view.get_all_cleaned_data = Mock(return_value=mock_cleaned_data)
        self.view.done(self.view.get_form_list)
        self.assertEqual(mock_save.call_count, 1)
        self.assertEqual(mock_redirect.call_count, 1)

    def test_build_forms_from_questionnaire(self):
        """
        _build_forms_from_questionnaire() should make form_list a dictionary with TempLanguageForm as the last form
        """
        self.view._build_forms_from_questionnaire()
        self.assertIsInstance(self.view.form_list, types.DictType)
        self.assertIs(self.view.form_list.get(str(len(self.view.form_list) - 1)), TempLanguageForm)


class TempLanguageUpdateViewTestCase(TestCase):
    def setUp(self):
        questionnaire = Questionnaire.objects.create(questions=[{"id": 0, "text": "question"}])
        self.obj = TempLanguage.objects.create(pk=999, code="tst", questionnaire=questionnaire)
        self.request = RequestFactory().get("/uw/templanguages/999/edit")
        self.request.user = create_user()
        self.view = setup_view(TempLanguageUpdateView(), self.request)

    def test_get_with_user(self):
        """
        Requesting TempLanguage update view should return successful response
        """
        response = TempLanguageUpdateView.as_view()(self.request, pk=999)
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

    def test_config(self):
        """
        Sanity check for view config
        """
        self.assertIs(self.view.model, TempLanguage)
        self.assertIs(self.view.form_class, TempLanguageForm)
        self.assertEqual(self.view.template_name, "resources/templanguage_form.html")

    def test_get_context_data(self):
        """
        Context must contain "code" and "edit" keys. Context["edit"] must be True
        """
        self.view.object = self.obj
        context = self.view.get_context_data()
        self.assertIn("code", context)
        self.assertIn("edit", context)
        self.assertTrue(context["edit"])

    def test_form_valid(self):
        """
        form.instance.modified_by must be a user object, represented by his username
        """
        form = Mock()
        form.cleaned_data = Mock()
        self.view.form_valid(form)
        self.assertIsInstance(form.instance.modified_by, User)
        self.assertEqual(form.instance.modified_by, self.request.user)


class AjaxTemporaryCodeTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/uw/ajax/templanguage/code/get/")
        self.request.user = create_user()

    def test_get(self):
        """
        Returned code should be in the format of 'qaa-x-??????', where ? is a-f or 0-9
        """
        response = AjaxTemporaryCode.as_view()(self.request)
        p = re.compile("^qaa-x-[a-f0-9]{6}$")
        self.assertIsNotNone(p.match(response.content))


class TempLanguageAdminViewTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="IETF")
        self.request = RequestFactory().get('/region_assignment/')
        self.request.user = create_user()
        self.request.user.groups.add(self.group)
        self.view = setup_view(TempLanguageAdminView(), self.request)

    @patch("td.views.TempLanguageAdminView.get_context_data", return_value={})
    def test_get_with_user_and_group(self, mock_get_context_data):
        """
        Requesting TempLanguage - Admin should return successful response
        """
        response = TempLanguageAdminView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    @patch("td.views.TempLanguageAdminView.get_context_data", return_value={})
    def test_get_without_group(self, mock_get_context_data):
        """
        Requesting TempLanguage - Admin without the right group should return redirect
        """
        self.request.user.groups.remove(self.group)
        response = TempLanguageAdminView.as_view()(self.request)
        self.assertEqual(response.status_code, 302)

    def test_config(self):
        """
        Sanity check for view config
        """
        self.assertEqual(self.view.template_name, "resources/templanguage_admin.html")

    def test_get_context_data(self):
        """
        Context should contain "pending" key
        """
        TempLanguage.objects.create(pk=999, code="abc")
        returned = self.view.get_context_data()
        self.assertIn("pending", returned)


class GatewayLanguagesAutocompleteTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse("gateway_languages"))
        self.ol = Language.objects.create(code="ol", iso_639_3="tol", name="Test Other Language",
                                          gateway_flag=False)
        self.gl = Language.objects.create(code="gl", iso_639_3="tgl", name="Test Gateway Language",
                                          gateway_flag=True)

    def test_returns_json(self):
        response = gateway_languages_autocomplete(self.request)
        self.assertIsInstance(response, JsonResponse)
        self.assertIn("results", response.content)
        self.assertIn("count", response.content)
        self.assertIn("term", response.content)

    @patch("td.views.Language.get_gateway_languages")
    def test_call_get_gateway_languages(self, mock_get_gateway_languages):
        gateway_languages_autocomplete(self.request)
        mock_get_gateway_languages.assert_called_once_with()

    def test_search_other_language(self):
        term = "ol"
        expected_results = []
        request = RequestFactory().get("/ac/gateway-langnames/?q=" + term)
        response = gateway_languages_autocomplete(request)
        data = json.loads(response.content)
        self.assertListEqual(data.get("results"), expected_results)
        self.assertEqual(data.get("term"), "ol")
        self.assertEqual(data.get("count"), 0)

    def test_search_gateway_language(self):
        term = "gl"
        expected_results = [dict(pk=self.gl.pk, lc=self.gl.lc, ln=self.gl.ln, lr=self.gl.lr, ang=self.gl.ang)]
        request = RequestFactory().get("/ac/gateway-langnames/?q=" + term)
        response = gateway_languages_autocomplete(request)
        data = json.loads(response.content)
        self.assertListEqual(data.get("results"), expected_results)
        self.assertEqual(data.get("term"), term)
        self.assertEqual(data.get("count"), 1)
