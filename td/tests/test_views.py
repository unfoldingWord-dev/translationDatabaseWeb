import re

from mock import Mock, patch

from django.test import TestCase
from django.contrib.auth.models import User

from djcelery.tests.req import RequestFactory

from td.models import TempLanguage
from td.views import TempLanguageListView, TempLanguageDetailView, AjaxTemporaryCode, TempLanguageAdminView


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


class TempLanguageListViewTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/uw/templanguages/")
        self.request.user = create_user()
        self.view = setup_view(TempLanguageListView(), self.request)

    def test_get_with_user(self):
        """
        Requesting TempLanguage list should return successful response
        """
        response = TempLanguageAdminView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for view config
        """
        self.assertIs(self.view.model, TempLanguage)
        self.assertEqual(self.view.template_name, "resources/templanguage_list.html")


class TempLanguageDetailViewTestCase(TestCase):
    def setUp(self):
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
        self.request = RequestFactory().get('/region_assignment/')
        self.request.user = create_user()
        self.view = setup_view(TempLanguageAdminView(), self.request)

    @patch("td.views.TempLanguageAdminView.get_context_data")
    def test_get_with_user(self, mock_get_context_data):
        """
        Requesting TempLanguage - Admin should return successful response
        """
        mock_get_context_data.return_value = {}
        response = TempLanguageAdminView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

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
