from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from td.tracking.views import HomeView

class HomeViewTestCase(TestCase):

	def setUp(self):
		self.factory = RequestFactory()
		self.user, _ = User.objects.get_or_create(
			username="test_user",
			email="test@gmail.com",
			password="test_password",
		)
		self.setup_view = function(view, request, *args, **kwargs)

	def test_get(self):
		request = self.factory.get('/tracking/')
		request.user = self.user
		response = HomeView.as_view()(request)
		self.assertEqual(response.status_code, 200)