from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.utils import timezone

from td.tracking.views import *
from td.tracking.models import Charter, Department
from td.tracking.forms import *
from td.models import Language

from mock import patch, Mock


def setup_view(view, request, *args, **kwargs):
    """
    Mimic as_view() by returning the view instance.
    args and kwargs are the same as you would pass to reverse()
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


# ------------------------------- #
#            MISC VIEWS           #
# ------------------------------- #


class HomeViewTestCase(TestCase):

    def setUp(self):
        user, _ = User.objects.get_or_create(
            username="test_user",
            email="test@gmail.com",
            password="test_password",
        )
        self.request = RequestFactory().get('/tracking/')
        self.request.user = user

    def test_get(self):
        """
        Sanity check against errors when going to tracking home page
        """
        response = HomeView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        """
        Template name should be correct
        """
        view = setup_view(HomeView(), self.request)
        self.assertEqual(view.template_name, "tracking/project_list.html")


# ---------------------------------- #
#            CHARTER VIEWS           #
# ---------------------------------- #


class CharterAddViewTestCase(TestCase):

    def setUp(self):
        user, _ = User.objects.get_or_create(
            username="test_user",
            email="test@gmail.com",
            password="test_password",
        )
        self.request = RequestFactory().get('/tracking/charter/new/')
        self.request.user = user
        self.view = setup_view(CharterAddView(), self.request)

    def test_get(self):
        """
        Sanity check against errors when going to single charter form
        """
        response = CharterAddView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        """
        Template name should be correct
        """
        self.assertEqual(self.view.template_name, "tracking/charter_form.html")

    def test_model(self):
        """
        Model for CharterAddView should be Charter
        """
        self.assertIs(self.view.model, Charter)

    def test_form_class(self):
        """
        Form class for CharterAddView should be CharterForm
        """
        self.assertIs(self.view.form_class, CharterForm)

    def test_get_initial(self):
        """
        get_initial() should return today's date and logged-in user's username
        """
        initial = self.view.get_initial()
        self.assertEqual(initial["start_date"], timezone.now().date())
        self.assertEqual(initial["created_by"], "test_user")

    @patch("td.tracking.forms.CharterForm")
    def test_form_valid(self, form):
        """
        form_valid() should call save() and redirect to the success page with object's type and ID as args
        """
        form.save = Mock(return_value=type("MockForm", (), {"id": 9999}))
        response = self.view.form_valid(form)
        form.save.assert_called_once_with()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/tracking/success/charter/9999/")


class CharterUpdateViewTestCase(TestCase):

    def setUp(self):
        user, _ = User.objects.get_or_create(
            username="test_user",
            email="test@gmail.com",
            password="test_password",
        )
        language, _ = Language.objects.get_or_create(
            id=9999,
            code="ts",
            name="Test Language",
        )
        department, _ = Department.objects.get_or_create(
            name="Test Department",
        )
        self.charter, _ = Charter.objects.get_or_create(
            id=9999,
            language=language,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
        )
        self.request = RequestFactory().get('/tracking/charter/update/')
        self.request.user = user
        self.view = setup_view(CharterUpdateView(), self.request, pk=9999)

    def test_get(self):
        """
        Sanity check against errors when going to edit charter form
        """
        response = CharterUpdateView.as_view()(self.request, pk=9999)
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        """
        Template name for CharterUpdateView should be charter_update_form.html
        """
        self.assertEqual(self.view.template_name_suffix, "_update_form")

    def test_model(self):
        """
        Model for CharterUpdateView should be Charter
        """
        self.assertIs(self.view.model, Charter)

    def test_form_class(self):
        """
        Form class for CharterUpdateView should be CharterForm
        """
        self.assertIs(self.view.form_class, CharterForm)

    @patch("td.tracking.forms.CharterForm")
    def test_form_valid(self, form):
        """
        form_valid() should call save() and redirect to the success page with object's type and ID as args
        """
        form.save = Mock(return_value=type("MockForm", (), {"id": 9999}))
        response = self.view.form_valid(form)
        form.save.assert_called_once_with()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/tracking/success/charter/9999/")


class NewCharterModalViewTestCase(TestCase):

    def setUp(self):
        user, _ = User.objects.get_or_create(
            username="test_user",
            email="test@gmail.com",
            password="test_password",
        )
        self.request = RequestFactory().get('/tracking/ajax/charter/modal/')
        self.request.user = user
        self.view = setup_view(NewCharterModalView(), self.request)

    def test_get(self):
        """
        Sanity check against errors when calling for a charter modal
        """
        response = NewCharterModalView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        """
        Template name for NewCharterModalView should be new_charter_modal.html
        """
        self.assertEqual(self.view.template_name, "tracking/new_charter_modal.html")

    @patch("td.tracking.forms.CharterForm")
    def test_form_valid(self, form):
        """
        form_valid() should call save() and render a success message
        """
        form.save = Mock(return_value=type("MockForm", (), {"id": 9999}))
        response = self.view.form_valid(form)
        form.save.assert_called_once_with()
        self.assertContains(response, "<p class=\"success\">Project charter has been created. Close this and try again.</p>", count=1, html=True)


class MultiCharterAddViewTestCase(TestCase):

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username="test_user",
            email="test@gmail.com",
            password="test_password",
        )
        self.request = RequestFactory().get("/tracking/mc/new/")
        self.request.user = self.user
        self.view = setup_view(MultiCharterAddView(), self.request)

    def test_get(self):
        """
        Sanity check against errors when going to multi-charter form
        """
        response = MultiCharterAddView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_get_factory_kwargs(self):
        """
        MultiCharterForm should be included in kwargs as "form"
        """
        kwargs = self.view.get_factory_kwargs()
        self.assertIs(kwargs["form"], MultiCharterForm)

    def test_get_initial(self):
        """
        get_initial() should give today's date for start_date and user's username for created_by
        """
        initial = self.view.get_initial()
        self.assertEqual(initial[0]["start_date"], timezone.now().date())
        self.assertEqual(initial[0]["created_by"], "test_user")

    def test_get_queryset(self):
        """
        get_queryset() should return an empty array
        """
        self.assertEqual(len(self.view.get_queryset()), 0)

    def test_construct_formset(self):
        """
        Language fields must have data-lang* attributes on POST
        """
        language, _ = Language.objects.get_or_create(
            id=1234,
            name="OneTwoThreeFour",
            code="ottf",
            country=None,
        )
        language, _ = Language.objects.get_or_create(
            id=5678,
            name="FiveSixSevenEight",
            code="fsse",
            country=None,
        )
        post_data = {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "0",
            "form-MAX_NUM_FORMS": "9999",
            "form-0-language": "1234",
            "form-1-language": "5678",
        }
        post = RequestFactory().post("/tracking/mc/new/", post_data)
        post.user = self.user
        post_view = setup_view(MultiCharterAddView(), post)
        output = post_view.construct_formset()
        widget_1 = output.forms[0].fields["language"].widget.attrs
        widget_2 = output.forms[1].fields["language"].widget.attrs
        self.assertEqual(widget_1["data-lang-pk"], 1234)
        self.assertEqual(widget_1["data-lang-ln"], "OneTwoThreeFour")
        self.assertEqual(widget_1["data-lang-lc"], "ottf")
        self.assertEqual(widget_1["data-lang-lr"], "")
        self.assertEqual(widget_2["data-lang-pk"], 5678)
        self.assertEqual(widget_2["data-lang-ln"], "FiveSixSevenEight")
        self.assertEqual(widget_2["data-lang-lc"], "fsse")
        self.assertEqual(widget_2["data-lang-lr"], "")

    def formset_valid(self):
        """
        messages.info() should be called with request and a message
        """
        pass
