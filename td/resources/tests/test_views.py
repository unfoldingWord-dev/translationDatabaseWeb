from mock import patch

from django.test import TestCase
from django.contrib.auth.models import User

from djcelery.tests.req import RequestFactory

from td.models import TempLanguage
from td.resources.views import TempLanguageQuestionnaireView


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


class TempLanguageQuestionnaireViewTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/region_assignment/')
        self.request.user = create_user()
        self.view = setup_view(TempLanguageQuestionnaireView(), self.request)

    @patch("td.resources.views.TempLanguageQuestionnaireView.get_context_data")
    def test_get_with_user(self, mock_get_context_data):
        """
        Requesting questionnaire of a temporary language should return successful response
        """
        mock_get_context_data.return_value = {}
        response = TempLanguageQuestionnaireView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for view config
        """
        self.assertEqual(self.view.template_name, "resources/questionnaire.html")

    def test_get_context_data(self):
        """
        Context must contain "obj" key
        """
        TempLanguage.objects.create(pk=999, code="abc")
        returned = self.view.get_context_data(temp_language=999)
        self.assertIn("obj", returned)
