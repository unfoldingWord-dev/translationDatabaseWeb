from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from mock import Mock, patch

from td.models import Language, WARegion
from td.gl_tracking.models import (
    Phase,
    DocumentCategory,
    Document,
    Progress
)
from td.gl_tracking.views import (
    HomeView,
    PhaseView,
    RegionDetailView,
    VariantSplitView,
    ProgressEditView,
    RegionAssignmentView,
)
from td.gl_tracking.forms import (
    VariantSplitModalForm,
    ProgressForm,
    RegionAssignmentModalForm,
)


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
        WARegion.objects.create(name="Test", slug="test")
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
        self.assertIs(self.view.model, WARegion)

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


class VariantSplitViewTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/ajax/variant_split_modal/')
        self.request.user = create_user()
        self.view = setup_view(VariantSplitView(), self.request)

    def test_get_with_user(self):
        """
        Sanity check against errors when going requesting phase view
        """
        Language.objects.create(code="test")
        response = VariantSplitView.as_view()(self.request, slug="test")
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertEqual(
            self.view.template_name,
            "gl_tracking/variant_split_modal_form.html"
        )
        self.assertIs(self.view.form_class, VariantSplitModalForm)

    def test_get_context_data(self):
        """
        language info should be in the context
        """
        Language.objects.create(code="test")
        self.view.object = None
        self.view.kwargs = {"slug": "test"}
        context = self.view.get_context_data()
        self.assertIn("language", context)

    @patch('td.gl_tracking.views.render')
    def test_form_valid(self, mock_render):
        """
        Render should be called once with the right URL and context that
           contains 'success', 'language', and 'variant' info
        """
        a = Language.objects.create(code="test")
        b = Language.objects.create(code="variant")
        b.variant_of = a
        b.save()

        self.view.kwargs = {"slug": "test"}
        form = Mock()
        form.data = {"variant": "variant"}

        self.view.form_valid(form)
        request, url, context = mock_render.call_args[0]
        self.assertIn("success", context)
        self.assertIn("language", context)
        self.assertIn("variant", context)
        self.assertEqual(url, "gl_tracking/variant_split_modal_form.html")
        self.assertEqual(mock_render.call_count, 1)


class ProgressEditViewTestCase(TestCase):
    def setUp(self):
        phase = Phase.objects.create(number="1")
        doc_cat = DocumentCategory.objects.create(
            name="Test Category",
            phase=phase
        )
        doc = Document.objects.create(
            name="Test Document",
            code="td",
            category=doc_cat
        )
        language = Language.objects.create(code="tl")
        Progress.objects.create(language=language, type=doc, pk=1)
        self.request = RequestFactory().post('/progress/change/')
        self.request.user = create_user()
        self.view = setup_view(ProgressEditView(), self.request)

    def test_get_with_user(self):
        """
        Sanity check against errors when going requesting phase view
        """
        response = ProgressEditView.as_view()(self.request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertIs(self.view.model, Progress)
        self.assertEqual(self.view.template_name_suffix, "_update_modal_form")
        self.assertIs(self.view.form_class, ProgressForm)

    @patch('td.gl_tracking.views.render')
    def test_form_valid(self, mock_render):
        """
        When form is valid:
            render should be called once w/ success and object info in context
            form.save should be called once
        """
        form = Mock()
        form.save = Mock(return_value={})

        self.view.form_valid(form)
        self.assertEqual(form.save.call_count, 1)
        _, url, context = mock_render.call_args[0]
        self.assertIn("success", context)
        self.assertIn("object", context)
        self.assertEqual(url, "gl_tracking/progress_update_modal_form.html")
        self.assertEqual(mock_render.call_count, 1)


class RegionAssignmentViewTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/region_assignment/')
        self.request.user = create_user()
        self.view = setup_view(RegionAssignmentView(), self.request)

    def test_get_with_user(self):
        """
        Sanity check against errors when going requesting region assignment
        """
        # Language.objects.create(code="test")
        response = RegionAssignmentView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertEqual(
            self.view.template_name,
            "gl_tracking/region_assignment_modal_form.html"
        )
        self.assertIs(self.view.form_class, RegionAssignmentModalForm)

    def test_get_context_data(self):
        """
        wa_regions, gl_directors, and gl_helpers info should be in the context
        """
        context = self.view.get_context_data()
        self.assertIn("wa_regions", context)
        self.assertIn("gl_directors", context)
        self.assertIn("gl_helpers", context)

    @patch('td.gl_tracking.views.render')
    def test_form_valid(self, mock_render):
        """
        Render should be called once with the right URL and context that
           contains 'success' info
        """
        form = Mock()
        form.data = {}
        self.view.form_valid(form)

        request, url, context = mock_render.call_args[0]

        self.assertIn("success", context)
        self.assertEqual(url, "gl_tracking/region_assignment_modal_form.html")
        self.assertEqual(mock_render.call_count, 1)
