from django.core.urlresolvers import reverse
from django.test import TestCase
from djcelery.tests.req import RequestFactory

from td.api.views import questionnaire_json, templanguages_json, lang_assignment_json, lang_assignment_changed_json
from td.models import Language, TempLanguage, Country
from td.resources.models import Questionnaire


class QuestionnaireJsonTestCase(TestCase):

    def setUp(self):
        lang = Language.objects.create(code="tst", name="test")
        Questionnaire.objects.create(language=lang, questions=[{"question": "some text"}])

    def test_get(self):
        """
        Request should successfully return a JsonResponse
        """
        request = RequestFactory().get(reverse("api:questionnaire"))
        response = questionnaire_json(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")


class TempLanguagesJsonTestCase(TestCase):

    def setUp(self):
        c = Country.objects.create(name="test")
        TempLanguage.objects.create(code="tst", name="test", country=c)

    def test_get(self):
        """
        Request should successfully return a JsonResponse
        """
        request = RequestFactory().get(reverse("api:templanguages"))
        response = templanguages_json(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")


class LangAssignmentJsonTestCase(TestCase):

    def setUp(self):
        TempLanguage.objects.create(code="tst", name="test")

    def test_get(self):
        """
        Request should successfully return a JsonResponse
        """
        request = RequestFactory().get(reverse("api:templanguages_assignment"))
        response = lang_assignment_json(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")


class LangAssignmentChangedJsonTestCase(TestCase):

    def setUp(self):
        TempLanguage.objects.create(code="tst", name="test")

    def test_get(self):
        """
        Request should successfully return a JsonResponse
        """
        request = RequestFactory().get(reverse("api:templanguages_changed"))
        response = lang_assignment_changed_json(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
