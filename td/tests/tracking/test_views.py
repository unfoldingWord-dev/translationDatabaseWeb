import requests_mock
from mock import patch, Mock

from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.utils.importlib import import_module
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.urlresolvers import reverse

from td.tracking.views import *
from td.tracking.models import Charter, Department, Event
from td.tracking.forms import *
from td.models import Language


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

    def test_config(self):
        """
        Sanity check for config
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

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertEqual(self.view.template_name, "tracking/charter_form.html")
        self.assertIs(self.view.model, Charter)
        self.assertIs(self.view.form_class, CharterForm)

    def test_get_initial(self):
        """
        get_initial() should return today's date and logged-in user's username
        """
        initial = self.view.get_initial()
        self.assertEqual(initial["start_date"], timezone.now().date())
        self.assertEqual(initial["created_by"], "test_user")

    @patch("td.tracking.forms.CharterForm")
    def test_form_valid(self, mock_form):
        """
        form_valid() should call save() and redirect to the success page with object's type and ID as args
        """
        mock_form.save = Mock(return_value=type("MockForm", (), {"id": 9999}))
        response = self.view.form_valid(mock_form)
        mock_form.save.assert_called_once_with()
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

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertEqual(self.view.template_name_suffix, "_update_form")
        self.assertIs(self.view.model, Charter)
        self.assertIs(self.view.form_class, CharterForm)

    @patch("td.tracking.forms.CharterForm")
    def test_form_valid(self, mock_form):
        """
        form_valid() should call save() and redirect to the success page with object's type and ID as args
        """
        mock_form.save = Mock(return_value=type("MockForm", (), {"id": 9999}))
        response = self.view.form_valid(mock_form)
        mock_form.save.assert_called_once_with()
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

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertEqual(self.view.template_name, "tracking/new_charter_modal.html")

    @patch("td.tracking.forms.CharterForm")
    def test_form_valid(self, mock_form):
        """
        form_valid() should call save() and render a success message
        """
        mock_form.save = Mock(return_value=type("MockForm", (), {"id": 9999}))
        response = self.view.form_valid(mock_form)
        mock_form.save.assert_called_once_with()
        self.assertContains(response, "<p class=\"success\">Project charter has been created. Close this and try again.</p>", count=1, html=True)


class MultiCharterAddViewTestCase(TestCase):

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username="test_user",
            email="test@gmail.com",
            password="test_password",
        )
        self.request = RequestFactory().get("/tracking/mc/new/")
        setattr(self.request, "session", "session")
        setattr(self.request, "_messages", FallbackStorage(self.request))
        self.request.user = self.user
        self.view = setup_view(MultiCharterAddView(), self.request)

    def test_get(self):
        """
        Sanity check against errors when going to multi-charter form
        """
        response = MultiCharterAddView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check against wrong config
        """
        self.assertEqual(self.view.template_name, "tracking/multi_charter_form.html")
        self.assertIs(self.view.model, Charter)
        self.assertIs(self.view.form_class, MultiCharterForm)
        self.assertEqual(self.view.extra, 1)
        self.assertEqual(self.view.success_url, "/tracking/")

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

    @patch("td.tracking.forms.MultiCharterForm")
    @patch("td.tracking.views.messages")
    def test_formset_valid(self, mock_messages, mock_formset):
        """
        messages.info() should be called with request and a message
        """
        mock_messages.info = Mock()
        self.view.formset_valid(mock_formset)
        mock_messages.info.assert_called_once_with(self.request, "Your charters have been successfully created.")


# -------------------------------- #
#            EVENT VIEWS           #
# -------------------------------- #


class EventAddViewTestCase(TestCase):

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username="test_user",
            email="test@gmail.com",
            password="test_password",
        )
        self.request = RequestFactory().get('/tracking/event/new/')
        self.request.user = self.user
        setattr(self.request, "session", {})
        setattr(self.request, "_messages", FallbackStorage(self.request))
        self.view = setup_view(EventAddView(), self.request)

    def test_get(self):
        """
        Sanity check against errors when going to single event form
        """
        response = EventAddView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertIs(self.view.model, Event)
        self.assertIs(self.view.form_class, EventForm)

    def test_get_initial(self):
        """
        get_initial() should return today's date and logged-in user's username
        """
        initial = self.view.get_initial()
        self.assertEqual(initial["start_date"], timezone.now().date())
        self.assertEqual(initial["created_by"], "test_user")

    def test_get_form_kwargs(self):
        """
        If kwargs contains "pk", "pk" should be included in the returned kwargs
        """
        output = self.view.get_form_kwargs()
        self.assertNotIn("pk", output)

        self.view.kwargs["pk"] = 9999
        output = self.view.get_form_kwargs()
        self.assertIn("pk", output)

    @patch("td.tracking.views.get_facilitator_data")
    @patch("td.tracking.views.get_translator_data")
    @patch("td.tracking.views.get_material_data")
    def test_get_context_data(self, mock_get_material, mock_get_facilitator, mock_get_translator):
        """
        get_translator_data() should be called once
        get_facilitator_data() should be called once
        get_material_data() should be called once
        """
        self.view.object = Mock()
        self.view.get_context_data()
        mock_get_translator.assert_called_once_with(self.view)
        mock_get_facilitator.assert_called_once_with(self.view)
        mock_get_material.assert_called_once_with(self.view)

    @patch("td.tracking.views.messages")
    @patch("td.tracking.views.check_for_new_items")
    @patch("td.tracking.views.get_next_event_number")
    @patch("td.tracking.views.get_facilitator_ids")
    @patch("td.tracking.views.get_translator_ids")
    @patch("td.tracking.views.get_material_ids")
    @patch("td.tracking.forms.EventForm")
    def test_form_valid(self, mock_form, mock_material_ids, mock_translator_ids, mock_facilitator_ids, mock_next_number, mock_new_items, mock_messages):
        language, _ = Language.objects.get_or_create(
            id=9999,
            code="ts",
            name="Test Language",
        )
        department, _ = Department.objects.get_or_create(
            name="Test Department",
        )
        charter, _ = Charter.objects.get_or_create(
            id=9999,
            language=language,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
        )
        mock_event = type("MockEvent", (), {
            "id": 9999,
            "charter": charter,
            "translators": Mock(return_value=Mock(name="add")),
            "facilitators": Mock(return_value=Mock(name="add")),
            "materials": Mock(return_value=Mock(name="add")),
            "save": Mock()
        })
        mock_form.save.return_value = mock_event
        mock_translator_ids.return_value = []
        mock_facilitator_ids.return_value = []
        mock_material_ids.return_value = []
        mock_next_number.return_value = 9999

        # Scenario 1: no new items
        mock_new_items.return_value = []
        response = self.view.form_valid(mock_form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("tracking:charter_add_success", kwargs={"obj_type": "event", "pk": "9999"}))
        mock_form.save.assert_called_once_with()
        mock_translator_ids.assert_called_once_with([])
        mock_facilitator_ids.assert_called_once_with([])
        mock_material_ids.assert_called_once_with([])
        mock_event.translators.add.assert_called_once_with()
        mock_event.facilitators.add.assert_called_once_with()
        mock_event.materials.add.assert_called_once_with()
        mock_next_number.assert_called_once_with(charter)
        mock_new_items.assert_called_once_with(mock_event)

        # Scenario 2: new items found
        mock_new_items.return_value = ["test"]
        response = self.view.form_valid(mock_form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("tracking:new_item"))
        self.assertEqual(self.request.session["new_item_info"]["object"], "event")
        self.assertEqual(self.request.session["new_item_info"]["id"], [9999])
        self.assertEqual(self.request.session["new_item_info"]["fields"], ["test"])
        mock_messages.warning.assert_called_once_with(self.request, "Almost done! Your event has been saved. But...")

    # @requests_mock.mock()
    # @patch("td.tracking.views.redirect")
    # def test_form_valid_2(self, mock_redirect, mock_request):
    #     mock_form = Mock()
    #     self.view.form_valid(mock_form)
    #     mock_redirect.assert_called_once(reverse("tracking:charter_add_success"))


class EventUpdateViewTestCase(TestCase):

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
        event, _ = Event.objects.get_or_create(
            id=9999,
            charter=self.charter,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
        )
        self.request = RequestFactory().get('/tracking/event/edit/')
        self.request.user = user
        setattr(self.request, "session", {})
        setattr(self.request, "_messages", FallbackStorage(self.request))
        self.view = setup_view(EventUpdateView(), self.request, pk=9999)

    def test_get(self):
        """
        Sanity check against errors when going to edit an event form
        """
        response = EventUpdateView.as_view()(self.request, pk=9999)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertIs(self.view.model, Event)
        self.assertIs(self.view.form_class, EventForm)
        self.assertEqual(self.view.template_name_suffix, "_update_form")

    @patch("td.tracking.views.get_facilitator_data")
    @patch("td.tracking.views.get_translator_data")
    @patch("td.tracking.views.get_material_data")
    def test_get_context_data(self, mock_get_material, mock_get_facilitator, mock_get_translator):
        """
        get_translator_data() should be called once
        get_facilitator_data() should be called once
        get_material_data() should be called once
        """
        self.view.object = Mock()
        self.view.get_context_data()
        mock_get_translator.assert_called_once_with(self.view)
        mock_get_facilitator.assert_called_once_with(self.view)
        mock_get_material.assert_called_once_with(self.view)

    @patch("td.tracking.views.messages")
    @patch("td.tracking.views.check_for_new_items")
    @patch("td.tracking.views.get_next_event_number")
    @patch("td.tracking.views.get_facilitator_ids")
    @patch("td.tracking.views.get_translator_ids")
    @patch("td.tracking.views.get_material_ids")
    @patch("td.tracking.forms.EventForm")
    def test_form_valid(self, mock_form, mock_material_ids, mock_translator_ids, mock_facilitator_ids, mock_next_number, mock_new_items, mock_messages):
        mock_event = type("MockEvent", (), {
            "id": 9999,
            "charter": self.charter,
            "translators": Mock(return_value={Mock(name="add"), Mock(name="clear")}),
            "facilitators": Mock(return_value={Mock(name="add"), Mock(name="clear")}),
            "materials": Mock(return_value={Mock(name="add"), Mock(name="clear")}),
            "save": Mock()
        })
        mock_form.save.return_value = mock_event
        mock_translator_ids.return_value = []
        mock_facilitator_ids.return_value = []
        mock_material_ids.return_value = []
        mock_next_number.return_value = 9999

        # Scenario 1: no new items
        mock_new_items.return_value = []
        response = self.view.form_valid(mock_form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("tracking:charter_add_success", kwargs={"obj_type": "event", "pk": "9999"}))
        mock_form.save.assert_called_once_with()
        mock_translator_ids.assert_called_once_with([])
        mock_facilitator_ids.assert_called_once_with([])
        mock_material_ids.assert_called_once_with([])
        mock_event.translators.clear.assert_called_once_with()
        mock_event.facilitators.clear.assert_called_once_with()
        mock_event.materials.clear.assert_called_once_with()
        mock_event.translators.add.assert_called_once_with()
        mock_event.facilitators.add.assert_called_once_with()
        mock_event.materials.add.assert_called_once_with()
        mock_new_items.assert_called_once_with(mock_event)

        # Scenario 2: new items found
        mock_new_items.return_value = ["test"]
        response = self.view.form_valid(mock_form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("tracking:new_item"))
        self.assertEqual(self.request.session["new_item_info"]["object"], "event")
        self.assertEqual(self.request.session["new_item_info"]["id"], [9999])
        self.assertEqual(self.request.session["new_item_info"]["fields"], ["test"])
        mock_messages.warning.assert_called_once_with(self.request, "Almost done! Your event has been saved. But...")


class EventDetailViewTestCase(TestCase):

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
        event, _ = Event.objects.get_or_create(
            id=9999,
            charter=self.charter,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
        )
        self.request = RequestFactory().get('/tracking/event/detail/')
        self.request.user = user
        self.view = setup_view(EventDetailView(), self.request, pk=9999)

    def test_get(self):
        """
        Sanity check against errors when going to event detail page
        """
        response = EventDetailView.as_view()(self.request, pk=9999)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertIs(self.view.model, Event)


class MultiCharterEventViewTestCase(TestCase):

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username="test_user",
            email="test@gmail.com",
            password="test_password",
        )
        self.request = RequestFactory().get('/tracking/mc-event/new/')
        self.request.user = self.user
        # SessionWizardView will try to use session. Setting session up here.
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        setattr(self.request, "session", store)
        # Mocking messages framework so the view can use it
        setattr(self.request, "_messages", FallbackStorage(self.request))
        self.view = setup_view(MultiCharterEventView(), self.request)

    def test_get(self):
        """
        Sanity check against errors when going to multi-charter event form
        """
        response = MultiCharterEventView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertEqual(self.view.template_name, "tracking/multi_charter_event_form.html")
        self.assertEqual(self.view.form_list, [MultiCharterStarter, MultiCharterEventForm2])
        self.assertEqual(self.view.initial_dict, {"1": {"start_date": timezone.now().date()}})

    @patch("td.tracking.views.MultiCharterEventForm2")
    def test_get_context_data(self, mock_form_2):
        post_data = {
            "translator0": "Test Translator",
            "facilitator0": "Test Facilitator",
            "is_lead0": True,
            "speaks_gl0": True,
            "material0": "Test Material",
            "licensed0": True,
        }
        self.request = RequestFactory().post('/tracking/mc-event/new/', post_data)
        self.view = setup_view(MultiCharterEventView(), self.request)
        # For some reason, super's get_context_data() will look for the following attributes
        self.view.storage = lambda: None
        setattr(self.view.storage, "extra_data", {})
        self.view.steps = lambda: None
        setattr(self.view.steps, "current", "1")
        self.view.prefix = "multi_charter_event_form"
        #
        context = self.view.get_context_data(mock_form_2)
        #
        self.assertEqual(context["translators"][0], {"name": "Test Translator"})
        self.assertEqual(context["facilitators"][0], {"name": "Test Facilitator", "is_lead": True, "speaks_gl": True})
        self.assertEqual(context["materials"][0], {"name": "Test Material", "licensed": True})

    @patch("td.tracking.views.Language.objects.get")
    def test_get_form(self, mock_get):
        """
        In step 0 without POST, the form returned should be MultiCharterStarter
        In step 0 with POST, the form returned should MultiCharterEventForm1
        In step 1, the form returned should be MultiCharterEventForm2
        """
        self.assertIsInstance(self.view.get_form(step=0), MultiCharterStarter)

        # instance_dict will be accessed by an internal code
        self.view.instance_dict = {"1": Event}
        self.assertIsInstance(self.view.get_form(step=1), MultiCharterEventForm2)

        language = lambda: None
        setattr(language, "id", "9999")
        setattr(language, "ln", "Test Language")
        setattr(language, "lc", "tl")
        setattr(language, "lr", "Test Region")
        setattr(language, "gateway_flag", True)
        mock_get.return_value = language
        post_data = {"0-language": "9999"}
        self.request = RequestFactory().post('/tracking/mc-event/new/', post_data)
        self.view = setup_view(MultiCharterEventView(), self.request)
        self.assertIsInstance(self.view.get_form(step="0", data=post_data), MultiCharterEventForm1)

    def test_done(self):
        form_list = []
        form_dict = {}
        output = self.view.done(form_list, form_dict)
        print '\nOUTPUT', output
        pass
