import uuid
import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from djcelery.tests.req import RequestFactory

from td.api.views import questionnaire_json, templanguages_json, lang_assignment_json, lang_assignment_changed_json
from td.models import Language, TempLanguage, Country
from td.resources.models import Questionnaire


class QuestionnaireJsonTestCase(TestCase):

    def setUp(self):
        Country.objects.create(name="narnia")
        lang = Language.objects.create(code="tst", name="test")
        questions = [
            {
                "sort": 1,
                "help": "Test help text",
                "depends_on": None,
                "required": True,
                "text": "What do you call your language?",
                "input_type": "string",
                "id": 0
            },
            {
                "sort": 2,
                "help": "",
                "depends_on": None,
                "required": True,
                "text": "What country are you in?",
                "input_type": "string",
                "id": 1
            }
        ]
        field_mapping = {"0": "name", "1": "country"}
        self.questionnaire = Questionnaire.objects.create(pk=999, language=lang, questions=json.dumps(questions),
                                                          field_mapping=field_mapping)

    def test_get(self):
        """
        Request should successfully return a JsonResponse
        """
        request = RequestFactory().get(reverse("api:questionnaire"))
        response = questionnaire_json(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_post_success(self):
        """
        JSON response of success should be returned if the data looks good
        """
        data = {
            "request_id": uuid.uuid1(),
            "temp_code": "qaa-x-abcdef",
            "questionnaire_id": self.questionnaire.id,
            "app": "ts-android",
            "requester": "test requester",
            "answers": json.dumps([{"question_id": "0", "text": "answer"}, {"question_id": "1", "text": "narnia"}])
        }
        request = RequestFactory().post(reverse("api:questionnaire"), data=data)
        response = questionnaire_json(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        content = json.loads(response.content)
        self.assertIn("status", content)
        self.assertIn("message", content)
        self.assertEqual(content["status"], "success")
        self.assertGreater(len(content["message"]), 0)

    def test_post_error_country(self):
        """
        JSON response with an error status and descriptive message should be returned if no country matches the answer
        """
        data = {
            "request_id": uuid.uuid1(),
            "temp_code": "qaa-x-abcdef",
            "questionnaire_id": self.questionnaire.id,
            "app": "ts-android",
            "requester": "test requester",
            "answers": json.dumps([{"question_id": "0", "text": "answer"}, {"question_id": "1", "text": "oz"}])
        }
        request = RequestFactory().post(reverse("api:questionnaire"), data=data)
        content = json.loads(questionnaire_json(request).content)
        self.assertEqual(content["status"], "error")
        self.assertGreater(len(content["message"]), 0)
        self.assertIn("Country", content["message"])

    def test_post_error_questionnaire(self):
        """
        JSON response with an error status and descriptive message should be returned if no questionnaire matches the
            questionnaire_id value
        """
        data = {
            "request_id": uuid.uuid1(),
            "temp_code": "qaa-x-abcdef",
            "questionnaire_id": 831,
            "app": "ts-android",
            "requester": "test requester",
            "answers": json.dumps([{"question_id": "0", "text": "answer"}, {"question_id": "1", "text": "narnia"}])
        }
        request = RequestFactory().post(reverse("api:questionnaire"), data=data)
        content = json.loads(questionnaire_json(request).content)
        self.assertEqual(content["status"], "error")
        self.assertGreater(len(content["message"]), 0)
        self.assertIn("Questionnaire", content["message"])

    def test_post_integrity_error(self):
        """
        If required field (like "app") is not included in POST, JSON response should return with an error status and
            descriptive  message
        """
        data = {
            "request_id": uuid.uuid1(),
            "questionnaire_id": self.questionnaire.id,
            "temp_code": "qaa-x-abcdef",
            "requester": "test requester",
            "answers": json.dumps([{"question_id": "0", "text": "answer"}, {"question_id": "1", "text": "narnia"}])
        }
        request = RequestFactory().post(reverse("api:questionnaire"), data=data)
        content = json.loads(questionnaire_json(request).content)
        self.assertEqual(content["status"], "error")
        self.assertGreater(len(content["message"]), 0)
        self.assertIn("app", content["message"])


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
