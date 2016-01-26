from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from mock import Mock

from td.models import Region
from td.gl_tracking.views import HomeView, PhaseView, RegionDetailView


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


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/tracking/')
        self.request.user = create_user()
        self.view = setup_view(HomeView(), self.request)

    def test_get_with_user(self):
        """
        Sanity check against errors when going to gl_tracking home page
        """
        response = HomeView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertEqual(self.view.template_name, "gl_tracking/dashboard.html")

    def test_get_context_data(self):
        """
        Phases should be in context
        """
        context = self.view.get_context_data()
        self.assertIn("phases", context)


class PhaseViewTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().post('/ajax/phase_progress/', {"phase": "1"})
        self.request.user = create_user()
        self.view = setup_view(PhaseView(), self.request)

    def test_post_with_user(self):
        """
        Sanity check against errors when going requesting phase view
        """
        self.view.get_context_data = Mock(return_value={})
        response = PhaseView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertEqual(self.view.template_name, "gl_tracking/_phase_view.html")

    def test_get_context_data(self):
        """
        phase, regions, overall_progress, can_edit info should be in the context
        """
        context = self.view.get_context_data()
        self.assertIn("phase", context)
        self.assertIn("regions", context)
        self.assertIn("overall_progress", context)
        self.assertIn("can_edit", context)


class RegionDetailViewTestCase(TestCase):
    def setUp(self):
        Region.objects.create(name="Test", slug="test")
        self.request = RequestFactory().get('/ajax/region_detail/')
        self.request.user = create_user()
        self.view = setup_view(RegionDetailView(), self.request)

    def test_get_with_user(self):
        """
        Sanity check against errors when going requesting phase view
        """
        self.view.get_context_data = Mock(return_value={})
        response = RegionDetailView.as_view()(self.request, slug="test")
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertEqual(self.view.template_name, "gl_tracking/_region_detail.html")

    def test_get_context_data(self):
        """
        directors info should be in the context
        """
        # To mock super().get_context_data()?
        self.view.object = Mock()
        self.view.object.gl_director_set = Mock(return_value={
            "all": Mock(return_value=[])
        })
        context = self.view.get_context_data()
        self.assertIn("directors", context)
