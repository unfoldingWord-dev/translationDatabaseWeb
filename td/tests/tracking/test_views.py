from mock import patch, Mock

from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.utils.importlib import import_module
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.urlresolvers import reverse

from td.tracking.views import (
    HomeView, CharterTableSourceView, EventTableSourceView,
    CharterAddView, CharterUpdateView, NewCharterModalView, MultiCharterAddView,
    EventAddView, EventUpdateView, EventDetailView, MultiCharterEventView,
    SuccessView, MultiCharterSuccessView, NewItemView,
)
from td.tracking.models import (
    Charter, Event,
    Department, Hardware, Software,
    TranslationMethod, Output, Publication,
    Network,
)
from td.tracking.forms import (
    CharterForm, MultiCharterForm,
    EventForm,
    MultiCharterStarter, MultiCharterEventForm1, MultiCharterEventForm2,
)
from td.models import Language


def setup_view(view, request=None, *args, **kwargs):
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


class CharterTableSourceViewTestCase(TestCase):

    def setUp(self):
        language0 = Language.objects.create(
            id=9999,
            code="ts",
            name="Test Language",
        )
        language1 = Language.objects.create(
            id=8888,
            code="ml",
            name="Mock Language",
        )
        department = Department.objects.create(
            name="Test Department",
        )
        self.charter0 = Charter.objects.create(
            id=9999,
            language=language0,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
        )
        self.charter1 = Charter.objects.create(
            id=8888,
            language=language1,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
        )

    def test_queryset(self):
        self.view = setup_view(CharterTableSourceView(), pk=9999)
        self.assertEqual(len(self.view.queryset), 1)
        self.assertEqual(self.view.queryset[0], self.charter0)

    def test_queryset_empty(self):
        self.view = setup_view(CharterTableSourceView())
        self.view.model = Charter
        self.assertEqual(len(self.view.queryset), 2)

    def test_filtered_data(self):
        self.request = RequestFactory().get('', {
            "search[value]": "test",
            "order[0][column]": "0"
        })
        self.view = setup_view(CharterTableSourceView(), self.request)
        self.view.model = Charter
        self.view.fields = ["language__name"]
        self.assertIn(self.charter0, self.view.filtered_data)

    def test_filtered_data_all(self):
        self.request = RequestFactory().get('', {
            "search[value]": "language",
            "order[0][column]": "0"
        })
        self.view = setup_view(CharterTableSourceView(), self.request)
        self.view.model = Charter
        self.view.fields = ["language__name"]
        result = self.view.filtered_data
        self.assertIn(self.charter0, result)
        self.assertIn(self.charter1, result)

    def test_filtered_data_short(self):
        self.request = RequestFactory().get('', {
            "search[value]": "l",
            "order[0][column]": "0"
        })
        self.view = setup_view(CharterTableSourceView(), self.request)
        self.view.model = Charter
        self.view.fields = ["language__name"]
        result = self.view.filtered_data
        self.assertIn(self.charter0, result)
        self.assertIn(self.charter1, result) 


class EventTableSourceViewTestCase(TestCase):

    def setUp(self):
        language = Language.objects.create(
            id=9999,
            code="ts",
            name="Test Language",
        )
        department = Department.objects.create(
            name="Test Department",
        )
        charter = Charter.objects.create(
            id=9999,
            language=language,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
        )
        self.event0 = Event.objects.create(
            charter=charter,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
            number=1,
        )
        self.event1 = Event.objects.create(
            charter=charter,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
            number=2,
        )

    def test_queryset(self):
        self.view = setup_view(EventTableSourceView(), pk=9999)
        qs = self.view.queryset
        self.assertEqual(len(qs), 2)
        self.assertIn(self.event0, qs)
        self.assertIn(self.event1, qs)

    def test_queryset_empty(self):
        self.view = setup_view(EventTableSourceView())
        self.view.model = Event
        self.assertEqual(len(self.view.queryset), 2)

    def test_filtered_data(self):
        self.request = RequestFactory().get('', {
            "search[value]": "1",
            "order[0][column]": "0"
        })
        self.view = setup_view(EventTableSourceView(), self.request)
        self.view.model = Event
        self.view.fields = ["number"]
        self.assertIn(self.event0, self.view.filtered_data)

    def test_filtered_data_all(self):
        self.request = RequestFactory().get('', {
            "search[value]": "",
            "order[0][column]": "0"
        })
        self.view = setup_view(EventTableSourceView(), self.request)
        self.view.model = Event
        self.view.fields = ["number"]
        result = self.view.filtered_data
        self.assertIn(self.event0, result)
        self.assertIn(self.event1, result)


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
        mock_form.save = Mock(return_value=Mock(id=9999, save=Mock()))
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

        language = Mock(
            id="9999",
            ln="Test Language",
            lc="tl",
            lr="Test Region",
            gateway_flag=True,
        )
        mock_get.return_value = language
        post_data = {"0-language": "9999"}
        self.request = RequestFactory().post('/tracking/mc-event/new/', post_data)
        self.view = setup_view(MultiCharterEventView(), self.request)
        self.assertIsInstance(self.view.get_form(step="0", data=post_data), MultiCharterEventForm1)

    @patch("td.tracking.views.Charter.objects.get")
    @patch("td.tracking.views.Event.objects.create")
    @patch("td.tracking.views.get_next_event_number")
    @patch("td.tracking.views.check_for_new_items")
    @patch("td.tracking.views.messages.warning")
    def test_done(self, mock_warning, mock_new_items, mock_next_number, mock_event_create, mock_charter_get):
        #
        mock_cleaned_data = {
            "0-language_0": "9999",
            "0-language_1": "8888",
        }
        self.view.get_all_cleaned_data = Mock(return_value=mock_cleaned_data)
        #
        mock_event = Mock()
        mock_event.save = Mock()
        mock_event.hardware = Mock(add=Mock())
        mock_event.software = Mock(add=Mock())
        mock_event.networks = Mock(add=Mock())
        mock_event.departments = Mock(add=Mock())
        mock_event.translation_methods = Mock(add=Mock())
        mock_event.publication = Mock(add=Mock())
        mock_event.output_target = Mock(add=Mock())
        mock_event.facilitators = Mock(add=Mock())
        mock_event.translators = Mock(add=Mock())
        mock_event.materials = Mock(add=Mock())
        mock_event_create.return_value = mock_event
        #
        mock_new_items.return_value = []
        response = self.view.done({}, {})
        #
        calls = mock_charter_get.call_args_list
        self.assertEqual(len(calls), 2)  # Implies that mock_charter_get is called 2x
        calls[0].assert_called_once_with(pk="9999")
        calls[1].assert_called_once_with(pk="8888")
        self.assertEqual(mock_event_create.call_count, 2)
        self.assertEqual(mock_event.hardware.add.call_count, 2)
        self.assertEqual(mock_event.software.add.call_count, 2)
        self.assertEqual(mock_event.networks.add.call_count, 2)
        self.assertEqual(mock_event.departments.add.call_count, 2)
        self.assertEqual(mock_event.translation_methods.add.call_count, 2)
        self.assertEqual(mock_event.publication.add.call_count, 2)
        self.assertEqual(mock_event.output_target.add.call_count, 2)
        self.assertEqual(mock_event.facilitators.add.call_count, 2)
        self.assertEqual(mock_event.translators.add.call_count, 2)
        self.assertEqual(mock_event.materials.add.call_count, 2)
        self.assertEqual(mock_event.save.call_count, 2)
        self.assertEqual(mock_next_number.call_count, 2)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("tracking:multi_charter_success"))
        self.assertTrue(self.view.request.session._session["mc-event-success-charters"])

        mock_new_items.return_value = ["facilitators", "translators"]
        response = self.view.done({}, {})
        self.assertTrue(self.view.request.session._session["new_item_info"])
        self.assertTrue(mock_warning.call_count, 1)
        # Only care about the first argument when calling messages.warning
        self.assertEqual(mock_warning.call_args[0][0], self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("tracking:new_item"))


# ---------------------------------- #
#            SUCCESS VIEWS           #
# ---------------------------------- #


class SuccessViewTestCase(TestCase):

    def setUp(self):
        user, _ = User.objects.get_or_create(
            username="test_user",
            email="test@gmail.com",
            password="test_password",
        )
        language = Language.objects.create(
            id=9999,
            code="ts",
            name="Test Language",
        )
        department = Department.objects.create(
            name="Test Department",
        )
        self.charter = Charter.objects.create(
            id=9999,
            language=language,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
        )
        self.event = Event.objects.create(
            id=9999,
            charter=self.charter,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
        )
        self.request = RequestFactory().get('/tracking/success/')
        self.request.user = user
        self.view = setup_view(SuccessView(), self.request, obj_type="charter", pk=9999)

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertEqual(self.view.template_name, "tracking/charter_add_success.html")

    def test_get_no_allowed(self):
        """
        SuccessView should redirect to home page if referrer is not recognized
        """
        self.request.META["HTTP_REFERER"] = "wrong/url"
        response = SuccessView.as_view()(self.request, obj_type="charter", pk=9999)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("tracking:project_list"))

    def test_get_allowed(self):
        """
        SuccessView should be successfull if referrer is recognized
        """
        self.request.META["HTTP_REFERER"] = reverse("tracking:charter_add")
        response = SuccessView.as_view()(self.request, obj_type="charter", pk=9999)
        self.assertEqual(response.status_code, 200)

    def test_get_context_data_charter(self):
        """
        get_context_data needs to return the right context based on obj_type and pk kwargs
        """
        result = self.view.get_context_data(obj_type="charter", pk=9999)
        self.assertEqual(result["obj_type"], "charter")
        self.assertEqual(result["language_id"], 9999)
        self.assertEqual(result["status"], "Success")

    def test_get_context_data_event(self):
        """
        get_context_data needs to return the right context based on obj_type and pk kwargs
        """
        result = self.view.get_context_data(obj_type="event", pk=9999)
        self.assertEqual(result["obj_type"], "event")
        self.assertEqual(result["language_id"], 9999)
        self.assertEqual(result["status"], "Success")

    def test_get_context_data_wrong(self):
        """
        get_context_data needs to return the right context based on obj_type and pk kwargs
        """
        result = self.view.get_context_data(obj_type="wrong", pk=9999)
        self.assertEqual(result["obj_type"], "wrong")
        self.assertEqual(result["status"], "Sorry :(")


class MultiCharterSuccessViewTestCase(TestCase):

    def setUp(self):
        user, _ = User.objects.get_or_create(
            username="test_user",
            email="test@gmail.com",
            password="test_password",
        )
        language = Language.objects.create(
            id=9999,
            code="ts",
            name="Test Language",
        )
        department = Department.objects.create(
            name="Test Department",
        )
        self.charter = Charter.objects.create(
            id=9999,
            language=language,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
        )
        self.event = Event.objects.create(
            id=9999,
            charter=self.charter,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
        )
        self.request = RequestFactory().get('/tracking/success/mc-event/')
        self.request.user = user
        setattr(self.request, "session", {})
        self.view = setup_view(MultiCharterSuccessView(), self.request)

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertEqual(self.view.template_name, "tracking/multi_charter_success.html")

    def test_get_no_allowed(self):
        """
        MultiCharterSuccessView should redirect to home page if referrer is not recognized
        """
        self.request.META["HTTP_REFERER"] = "wrong/url"
        response = MultiCharterSuccessView.as_view()(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("tracking:project_list"))

    def test_get_allowed(self):
        """
        MultiCharterSuccessView should be successfull if referrer is recognized
        """
        self.request.META["HTTP_REFERER"] = reverse("tracking:multi_charter_event_add")
        response = MultiCharterSuccessView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_get_context_data_charter(self):
        """
        get_context_data needs to return the right context based on obj_type and pk kwargs
        """
        self.request.session["mc-event-success-charters"] = "something"
        self.view = setup_view(MultiCharterSuccessView(), self.request)
        result = self.view.get_context_data()
        self.assertEqual(result["charters"], "something")


class NewItemViewTestCase(TestCase):
    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username="test_user",
            email="test@gmail.com",
            password="test_password",
        )
        self.request = RequestFactory().get('/tracking/new_item/')
        self.request.user = self.user
        setattr(self.request, "session", {})
        setattr(self.request, "_messages", FallbackStorage(self.request))
        self.view = setup_view(NewItemView(), self.request)

    @patch("td.tracking.views.NewItemView.get_form")
    def test_get(self, mock_get_form):
        """
        Sanity check against errors when fetching a new item form
        """
        response = NewItemView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_config(self):
        """
        Sanity check for config
        """
        self.assertEqual(self.view.template_name, "tracking/new_item_form.html")
        self.assertIs(self.view.field_model_map["event"], Event)
        self.assertIs(self.view.field_model_map["hardware"], Hardware)
        self.assertIs(self.view.field_model_map["software"], Software)
        self.assertIs(self.view.field_model_map["translation_methods"], TranslationMethod)
        self.assertIs(self.view.field_model_map["output_target"], Output)
        self.assertIs(self.view.field_model_map["publication"], Publication)
        self.assertIs(self.view.field_model_map["networks"], Network)
        self.assertTrue(self.view.field_label_map["translation_methods"])
        self.assertTrue(self.view.field_label_map["hardware"])
        self.assertTrue(self.view.field_label_map["software"])
        self.assertTrue(self.view.field_label_map["networks"])
        self.assertTrue(self.view.field_label_map["output_target"])
        self.assertTrue(self.view.field_label_map["publication"])

    def test_get_context_data(self):
        """
        """
        self.assertIn("new_item_info", self.view.get_context_data())

    def test_get_form_get(self):
        """
        """
        self.view.request.session["new_item_info"] = {
            "fields": ["publication"],
            "id": 9999,
        }
        form = self.view.get_form()
        self.assertIn("publication", form.fields)

    def test_get_form_post(self):
        """
        """
        post_data = {
            "publication": "Test Publication"
        }
        post = RequestFactory().post('/tracking/new_item/', post_data)
        post.user = self.user
        setattr(post, "session", {})
        post_view = setup_view(NewItemView(), post)
        post_view.request.session["new_item_info"] = {
            "fields": ["publication"],
            "id": 9999,
        }
        form = post_view.get_form()
        self.assertIn("publication", form.fields)
        self.assertEqual(form.data["publication"], "Test Publication")

    @patch("td.tracking.views.messages.success")
    @patch("td.tracking.views.send_mail")
    def test_form_valid(self, mock_send_mail, mock_msg_success):
        """
        """
        mock_form = Mock()
        self.view.create_new_item = Mock()
        response = self.view.form_valid(mock_form)
        self.assertEqual(self.view.create_new_item.call_count, 1)
        self.assertEqual(mock_send_mail.call_count, 1)
        self.assertEqual(mock_msg_success.call_count, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("tracking:project_list"))

    # def test_create_new_item(self):
    #     info = {
    #         "fields": ["publication"],
    #         "id": [9999],
    #     }
    #     post = {
    #         "publication": "Test Publication"
    #     }
    #     response = self.view.create_new_item(info, post)
    #     print '\nRESPONSE:', response


class chartersAutocompleteTestCase(TestCase):
    # TODO
    pass


class chartersAutocompleteLidTestCase(TestCase):
    # TODO
    pass


class getTranslatorDataTestCase(TestCase):
    # TODO
    pass


class getFacilitatorDataTestCase(TestCase):
    # TODO
    pass


class getMaterialDataTestCase(TestCase):
    # TODO
    pass


class getTranslatorIdsTestCase(TestCase):
    # TODO
    pass


class getFacilitatorIdsTestCase(TestCase):
    # TODO
    pass


class getMaterialIdsTestCase(TestCase):
    # TODO
    pass


class checkForNewItemsTestCase(TestCase):
    # TODO
    pass


class getNextEventNumberTestCase(TestCase):
    # TODO
    pass
