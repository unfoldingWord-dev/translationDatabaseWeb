import operator
import re
import urlparse

from django import forms
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse as urlReverse
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import (
    CreateView,
    UpdateView,
    TemplateView,
    DetailView,
    FormView,
    View
)

from .forms import (
    CharterForm,
    EventForm,
    MultiCharterStarter,
    MultiCharterEventForm1,
    MultiCharterEventForm2,
    MultiCharterForm,
)
from .models import (
    Charter,
    Event,
    Facilitator,
    Material,
    Translator,
    TranslationMethod,
    Hardware,
    Software,
    Network,
    Output,
    Publication,
)
from td.models import Language, TempLanguage

from td.utils import DataTableSourceView
from account.mixins import LoginRequiredMixin
from formtools.wizard.views import SessionWizardView
from extra_views import ModelFormSetView


# ------------------------------- #
#            MISC VIEWS           #
# ------------------------------- #

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tracking/project_list.html"


class CharterTableSourceView(DataTableSourceView):

    @property
    def queryset(self):
        if "pk" in self.kwargs:
            return Charter.objects.filter(language=self.kwargs["pk"])
        elif "slug" in self.kwargs:
            return Charter.objects.filter(Q(language__wa_region__slug=self.kwargs["slug"]))
        else:
            return self.model._default_manager.all()

    @property
    def filtered_data(self):
        if self.search_term and len(self.search_term) <= 3:
            qs = self.queryset.filter(
                reduce(
                    operator.or_,
                    [Q(language__name__icontains=self.search_term) |
                     Q(language__code__icontains=self.search_term) |
                     Q(language__anglicized_name__icontains=self.search_term)]
                )
            ).order_by("start_date")
            if qs.count():
                return qs
        return self.queryset.filter(
            reduce(
                operator.or_,
                [Q(x) for x in self.filter_predicates]
            )
        ).order_by(
            self.order_by
        )


class EventTableSourceView(DataTableSourceView):

    @property
    def queryset(self):
        if "pk" in self.kwargs:
            return Event.objects.filter(charter=self.kwargs["pk"])
        else:
            return self.model._default_manager.all()

    @property
    def filtered_data(self):
        if self.search_term and len(self.search_term) <= 3:
            qs = self.queryset.filter(
                reduce(
                    operator.or_,
                    [Q(number__icontains=self.search_term)]
                )
            ).order_by("start_date")
            if qs.count():
                return qs
        return self.queryset.filter(
            reduce(
                operator.or_,
                [Q(x) for x in self.filter_predicates]
            )
        ).order_by(
            self.order_by
        )


class AjaxCharterListView(CharterTableSourceView):
    model = Charter
    fields = [
        "language__name",
        "language__anglicized_name",
        "language__code",
        "start_date",
        "end_date",
        "contact_person",
        "language__wa_region__name",
        "partner__name",
    ]
    # link is on column because name can't handle non-roman characters
    link_column = "language__code"
    link_url_name = "language_detail"
    link_url_field = "lang_id"


class AjaxCharterEventsListView(EventTableSourceView):
    model = Event
    fields = [
        "number",
        "location",
        "start_date",
        "end_date",
        "lead_dept__name",
        "contact_person",
    ]
    link_column = "number"
    link_url_name = "tracking:event_detail"
    link_url_field = "pk"


class FileDownloadView(LoginRequiredMixin, TemplateView):
    template_name = "tracking/file_download.html"


def downloadPDF(request, file_name):
    if request.user.is_authenticated():
        file = open('static/dist/files/{}'.format(file_name), 'rb')
        response = HttpResponse(file, content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename={}".format(file_name)
        return response
    else:
        return HttpResponseRedirect(urlReverse("tracking:project_list"))


# ---------------------------------- #
#            CHARTER VIEWS           #
# ---------------------------------- #


class CharterAddView(LoginRequiredMixin, CreateView):
    model = Charter
    form_class = CharterForm
    template_name = "tracking/charter_form.html"

    def get_initial(self):
        return {
            "language": self.kwargs.get("pk", None),
            "start_date": timezone.now().date(),
            "created_by": self.request.user.username,
        }

    def form_valid(self, form):
        self.object = form.save()
        return redirect("tracking:charter_add_success", obj_type="charter", pk=self.object.id)


class CharterUpdateView(LoginRequiredMixin, UpdateView):
    model = Charter
    form_class = CharterForm
    template_name_suffix = "_update_form"

    # Overidden to set initial values
    def get_initial(self):
        return {
            "modified_by": self.request.user.username
        }

    # Overridden to redirect upon valid submission
    def form_valid(self, form):
        self.object = form.save()
        self.object.modified_at = timezone.now()
        self.object.save()
        return redirect("tracking:charter_add_success", obj_type="charter", pk=self.object.id)


class NewCharterModalView(CharterAddView):
    template_name = 'tracking/new_charter_modal.html'

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, "tracking/new_charter_modal.html", {"success": True})


class MultiCharterAddView(LoginRequiredMixin, ModelFormSetView):
    template_name = "tracking/multi_charter_form.html"
    model = Charter
    form_class = MultiCharterForm
    extra = 1
    success_url = "/tracking/"

    def get_factory_kwargs(self):
        kwargs = super(MultiCharterAddView, self).get_factory_kwargs()
        kwargs["form"] = MultiCharterForm
        return kwargs

    def get_initial(self):
        return [{
            "start_date": timezone.now().date(),
            "created_by": self.request.user.username,
        }]

    def get_queryset(self):
        return Charter.objects.none()

    def construct_formset(self):
        formset = super(MultiCharterAddView, self).construct_formset()
        # Fill out data attrs needed by select2 to display user selection properly on POST
        if self.request.POST:
            for index in range(len(formset.forms)):
                language_pk = self.request.POST.get("form-" + str(index) + "-language")
                if language_pk:
                    language = Language.objects.get(pk=language_pk)
                    widget = formset.forms[index].fields["language"].widget.attrs
                    widget["data-lang-pk"] = language.pk
                    widget["data-lang-ln"] = language.ln
                    widget["data-lang-lc"] = language.lc
                    widget["data-lang-lr"] = language.lr
        return formset

    def formset_valid(self, formset):
        messages.info(self.request, "Your charters have been successfully created.")
        return super(MultiCharterAddView, self).formset_valid(formset)


# -------------------------------- #
#            EVENT VIEWS           #
# -------------------------------- #


class EventAddView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm

    # Overridden to include initial values
    def get_initial(self):
        return {
            "start_date": timezone.now().date(),
            "created_by": self.request.user.username,
        }

    # Overridden to pass URL argument to forms.py init()
    def get_form_kwargs(self, **kwargs):
        keywords = super(EventAddView, self).get_form_kwargs(**kwargs)
        if "pk" in self.kwargs:
            keywords["pk"] = self.kwargs["pk"]
        return keywords

    # Overridden to include custom dynamic data
    def get_context_data(self, *args, **kwargs):
        context = super(EventAddView, self).get_context_data(**kwargs)
        context["translators"] = get_translator_data(self)
        context["facilitators"] = get_facilitator_data(self)
        context["materials"] = get_material_data(self)
        context["view"] = "create"
        return context

    # Overridden to execute custom save and redirect upon valid submission
    def form_valid(self, form):
        event = self.object = form.save()

        # Add translators info
        translators = get_translator_data(self)
        translator_ids = get_translator_ids(translators)
        event.translators.add(*list(Translator.objects.filter(id__in=translator_ids)))

        # Add facilitators info
        facilitators = get_facilitator_data(self)
        facilitator_ids = get_facilitator_ids(facilitators)
        event.facilitators.add(*list(Facilitator.objects.filter(id__in=facilitator_ids)))

        # Add materials info
        materials = get_material_data(self)
        material_ids = get_material_ids(materials)
        event.materials.add(*list(Material.objects.filter(id__in=material_ids)))

        # Determine and set event number
        event.number = get_next_event_number(self.object.charter)
        event.save()

        # Check whether the user selected "Other" for one or more fields.
        # If he did, redirect him to NewItemForm with appropriate context info
        new_items = check_for_new_items(event)
        if len(new_items):
            self.request.session["new_item_info"] = {
                "object": "event",
                "id": [event.id],
                "fields": new_items,
            }
            messages.warning(self.request, "Almost done! Your event has been saved. But...")
            return redirect("tracking:new_item")
        else:
            return redirect("tracking:charter_add_success", obj_type="event", pk=self.object.id)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm

    # Overridden to include initial values
    def get_initial(self):
        return {
            "modified_by": self.request.user.username,
        }

    # Overridden to include custom dynamic data
    def get_context_data(self, *args, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        context["translators"] = get_translator_data(self)
        context["facilitators"] = get_facilitator_data(self)
        context["materials"] = get_material_data(self)
        context["view"] = "update"
        return context

    # Overridden to execute custom save and redirect upon valid submission
    def form_valid(self, form):
        event = self.object = form.save()

        # Update translators info
        translators = get_translator_data(self)
        translator_ids = get_translator_ids(translators)
        event.translators.clear()
        event.translators.add(*list(Translator.objects.filter(id__in=translator_ids)))

        # Add facilitators info
        facilitators = get_facilitator_data(self)
        facilitator_ids = get_facilitator_ids(facilitators)
        event.facilitators.clear()
        event.facilitators.add(*list(Facilitator.objects.filter(id__in=facilitator_ids)))

        # Add materials info
        materials = get_material_data(self)
        material_ids = get_material_ids(materials)
        event.materials.clear()
        event.materials.add(*list(Material.objects.filter(id__in=material_ids)))

        event.modified_at = timezone.now()
        event.save()

        # Check whether the user selected "Other" for one or more fields.
        # If he did, redirect him to NewItemForm with appropriate context info
        new_items = check_for_new_items(event)
        if len(new_items):
            self.request.session["new_item_info"] = {
                "object": "event",
                "id": [event.id],
                "fields": new_items,
            }
            messages.warning(self.request, "Almost done! Your event has been saved. But...")
            return redirect("tracking:new_item")
        else:
            return redirect("tracking:charter_add_success", obj_type="event", pk=self.object.id)


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event


class MultiCharterEventView(LoginRequiredMixin, SessionWizardView):
    template_name = 'tracking/multi_charter_event_form.html'
    form_list = [MultiCharterStarter, MultiCharterEventForm2]
    initial_dict = {
        "1": {"start_date": timezone.now().date()}
    }

    # Overridden to get the context for the dynamic data in step 2
    def get_context_data(self, form, **kwargs):
        context = super(MultiCharterEventView, self).get_context_data(form=form, **kwargs)
        if self.steps.current == "1":
            context["translators"] = get_translator_data(self)
            context["facilitators"] = get_facilitator_data(self)
            context["materials"] = get_material_data(self)
            context["charter_lookup"] = self.get_cleaned_data_for_step("0").get("0-language_0", "")
            context["view"] = "create"
        return context

    # Overridden to send a dynamic form based on user's input in step 1
    def get_form(self, step=None, data=None, files=None):
        if step is None:
            step = self.steps.current

        if step == "0" and self.request.POST:
            # Create array container for field names
            charter_fields = []
            # Iterate through post data...
            for key in sorted(data):
                # ... to look for our language fields and add them to the array
                if key.startswith("0-language"):
                    charter_fields.append(key)
            # Create a a dictionary of the field name and field definition for every language fields we have
            attrs = dict((field, forms.CharField(
                label="Charter",
                max_length=200,
                widget=forms.TextInput(
                    attrs={
                        "class": "language-selector-marked form-control",
                        "data-source-url": urlReverse("tracking:charters_autocomplete"),
                        "value": data[field],
                    }
                ),
                required=True,
            )) for field in charter_fields)
            # Dynamically create a new Form object with the field definitions
            NewForm = type("NewForm", (MultiCharterEventForm1,), attrs)
            # Bind modified posted data to the new form
            form = NewForm(data)
        else:
            # Otherwise, returns a form that would have been returned
            form = super(MultiCharterEventView, self).get_form(step, data, files)

        return form

    # This needs to be defined per requirements. This runs when all the steps are validated.
    def done(self, form_list, form_dict, **kwargs):
        data = self.get_all_cleaned_data()
        # Collect charters info from the first step
        charters = []
        for key in data:
            if key.startswith("0-language"):
                # No try..pass because the assumption is user can only select existing project charter
                charters.append(Charter.objects.get(pk=data[key]))
        # Container to collect info for success page
        charter_info = []
        # Containers to collect new_item_info, if any
        new_items = []
        ids = []
        # Create an event for each charter
        for charter in charters:
            event = Event.objects.create(
                charter=charter,
                location=data.get("location"),
                start_date=data.get("start_date"),
                end_date=data.get("end_date"),
                lead_dept=data.get("lead_dept"),
                current_check_level=data.get("current_check_level"),
                target_check_level=data.get("target_check_level"),
                contact_person=data.get("contact_person"),
                created_at=timezone.now(),
                created_by=self.request.user.username,
                number=get_next_event_number(charter),
            )
            event.save()
            # The cleaned data already has the list of object instances for these relationship fields
            event.hardware.add(*data.get("hardware", []))
            event.software.add(*data.get("software", []))
            event.networks.add(*data.get("networks", []))
            event.departments.add(*data.get("departments", []))
            event.translation_methods.add(*data.get("translation_methods", []))
            event.publication.add(*data.get("publication", []))
            event.output_target.add(*data.get("output_target", []))
            # Process and add dynamic facilitators info
            facilitators = get_facilitator_data(self)
            facilitator_ids = get_facilitator_ids(facilitators)
            event.facilitators.add(*list(Facilitator.objects.filter(id__in=facilitator_ids)))
            # Process and add dynamic translators info
            translators = get_translator_data(self)
            translator_ids = get_translator_ids(translators)
            event.translators.add(*list(Translator.objects.filter(id__in=translator_ids)))
            # Process and add dynamic materials info
            materials = get_material_data(self)
            material_ids = get_material_ids(materials)
            event.materials.add(*list(Material.objects.filter(id__in=material_ids)))

            # Collecting info for success page
            charter_info.append({"name": charter.language.name, "id": charter.language.id})
            # Collecting info for NewItemForm
            new_items = check_for_new_items(event)
            if len(new_items):
                ids.append(event.id)

        # Determine whether the user should be redirected to the success page or NewItemForm
        if len(new_items):
            self.request.session["new_item_info"] = {
                "object": "event",
                "id": ids,
                "fields": new_items,
            }
            messages.warning(self.request, "Almost done! Your event has been saved. But...")
            return redirect("tracking:new_item")
        else:
            self.request.session["mc-event-success-charters"] = charter_info
            return redirect("tracking:multi_charter_success")


# ---------------------------------- #
#            SUCCESS VIEWS           #
# ---------------------------------- #


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "tracking/charter_add_success.html"

    def get(self, request, *args, **kwargs):
        # Redirects user to tracking home page if he doesn't get here from new
        #    charter or event forms
        try:
            referer = request.META["HTTP_REFERER"]
        except KeyError:
            return redirect("tracking:project_list")

        allowed_urls = [
            re.compile(r"^{}$".format(urlReverse("tracking:charter_add"))),
            re.compile(r"^{}$".format(urlReverse("tracking:charter_update", kwargs={'pk': kwargs["pk"]}))),
            re.compile(r"^{}$".format(urlReverse("tracking:event_add"))),
            re.compile(r"^{}$".format(urlReverse("tracking:event_add_specific", kwargs={'pk': kwargs["pk"]}))),
            re.compile(r"^{}$".format(urlReverse("tracking:event_update", kwargs={'pk': kwargs["pk"]}))),
        ]

        path = urlparse.urlparse(referer).path

        if any(url.match(path) for url in allowed_urls):
            return super(SuccessView, self).get(self, *args, **kwargs)
        else:
            return redirect("tracking:project_list")

    def get_context_data(self, *args, **kwargs):
        # Append additional context to display custom message
        # NOTE: Maybe the logic for custom message should go in the template?
        context = super(SuccessView, self).get_context_data(**kwargs)
        context["link_id"] = kwargs["pk"]
        context["obj_type"] = kwargs["obj_type"]
        context["status"] = "Success"
        if kwargs["obj_type"] == "charter":
            charter = Charter.objects.get(pk=kwargs["pk"])
            context["language_id"] = charter.language.id
            context["message"] = "Project " + charter.language.name + " has been successfully added."
        elif kwargs["obj_type"] == "event":
            event = Event.objects.get(pk=kwargs["pk"])
            context["language_id"] = event.charter.language.id
            context["message"] = "Your event for " + event.charter.language.name + " has been successfully added."
        else:
            context["status"] = "Sorry :("
            context["message"] = "It seems like you got here by accident"
        return context


class MultiCharterSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "tracking/multi_charter_success.html"

    def get(self, request, *args, **kwargs):
        # Redirects user to tracking home page if he doesn't get here from new
        #    charter or event forms
        try:
            referer = request.META["HTTP_REFERER"]
        except KeyError:
            return redirect("tracking:project_list")

        allowed_urls = [
            re.compile(r"^{}$".format(urlReverse("tracking:multi_charter_event_add"))),
        ]

        path = urlparse.urlparse(referer).path

        if any(url.match(path) for url in allowed_urls):
            return super(MultiCharterSuccessView, self).get(self, *args, **kwargs)
        else:
            return redirect("tracking:project_list")

    def get_context_data(self, *args, **kwargs):
        # Append additional context to display custom message
        # NOTE: Maybe the logic for custom message should go in the template?
        context = super(MultiCharterSuccessView, self).get_context_data(**kwargs)
        context["charters"] = self.request.session.get("mc-event-success-charters", [])
        return context


class NewItemView(LoginRequiredMixin, FormView):
    template_name = "tracking/new_item_form.html"
    field_model_map = {
        "event": Event,
        "hardware": Hardware,
        "software": Software,
        "translation_methods": TranslationMethod,
        "output_target": Output,
        "publication": Publication,
        "networks": Network,
    }
    field_label_map = {
        "translation_methods": "Translation Methodology",
        "hardware": "Hardware Used",
        "software": "Software/App used",
        "networks": "Network",
        "output_target": "Output Target",
        "publication": "Publishing Means",
    }

    def get_context_data(self, *args, **kwargs):
        context = super(NewItemView, self).get_context_data(**kwargs)
        context["new_item_info"] = self.request.session.get("new_item_info", [])
        return context

    def get_form(self):
        object = self.request.session.get("new_item_info", {"fields": []})
        # Dynamically create a form class based on how many types of fields the user chose "Other" on
        attrs = {}
        for field in object["fields"]:
            attrs[field] = forms.CharField(
                label=self.field_label_map.get(field, "Unknown"),
                max_length=None,
                widget=forms.TextInput(
                    attrs={
                        "class": "new-items form-control",
                        "data-event": object["id"],
                    }
                ),
                required=False,
            )
        NewItemForm = type("NewItemForm", (forms.Form,), attrs)
        # Returns bound or unbound form. The form is remade at every POST or GET
        if self.request.POST:
            form = NewItemForm(self.request.POST)
        else:
            form = NewItemForm()
        return form

    def form_valid(self, form):
        self.create_new_item(self.request.session.get("new_item_info"), self.request.POST)
        send_mail(
            'tD New Item',
            'Some new items needs to be added to the event.' + str(self.request.POST),
            self.request.user.email,
            ['vleong2332@gmail.com'],
            fail_silently=False
        )
        messages.success(self.request, "Yes! Your submission info has been updated. If there's any problem with your submission, you'll be contacted via email by the admin.")
        return HttpResponseRedirect(urlReverse("tracking:project_list"))

    def create_new_item(self, info, post):
        # For each type of fields that contain new item...
        for field in info["fields"]:
            # Break the input into list of values of cleaned string
            data = post[field].split(',')
            for index in range(len(data)):
                data[index] = data[index].rstrip().lstrip().capitalize()
            # For each value that the user gives...
            for string in data:
                if len(string):
                    model = self.field_model_map.get(field, None)
                    # Assign item to be added to the answer. Don't create if it already exists.
                    try:
                        item = model.objects.get(name=string)
                    except model.DoesNotExist:
                        item = model.objects.create(name=string)
                    # Add item to every events that were created earlier
                    for id in info["id"]:
                        related_objs = getattr(Event.objects.get(pk=id), field, None)
                        related_objs.add(item)
                        try:
                            # Remove "Other" from the list of answer if it's still there
                            other = related_objs.get(name="Other")
                            related_objs.remove(other)
                        except:
                            # If "Other" is no longer a part of the answer, just skip through
                            pass


class AjaxCharterPartnerLookup(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            c = Charter.objects.get(pk=request.GET["pk"])
            return HttpResponse(c.partner_id or "")
        except Charter.DoesNotExist:
            return HttpResponse("")


# -------------------- #
#    VIEW FUNCTIONS    #
# -------------------- #


# Function: Returns a JSON response of charter and language info based on a search term
def charters_autocomplete(request):
    term = request.GET.get("q").lower().encode("utf-8")
    charters = Charter.objects.filter(Q(language__code__icontains=term) | Q(language__name__icontains=term))
    data = [
        {
            "pk": charter.id,
            "ln": charter.language.ln,
            "lc": charter.language.lc,
            "lr": charter.language.lr,
            "gl": charter.language.gateway_flag
        }
        for charter in charters
    ]
    return JsonResponse({"results": data, "count": len(data), "term": term})


# Function: Same like charters_autocomplete, but returns the id of the language, instead
#    of the charter
def charters_autocomplete_lid(request):
    term = request.GET.get("q").lower().encode("utf-8")
    charters = Charter.objects.filter(Q(language__code__icontains=term) | Q(language__name__icontains=term))
    data = [
        {
            "pk": charter.language.id,
            "ln": charter.language.ln,
            "lc": charter.language.lc,
            "lr": charter.language.lr,
            "gl": charter.language.gateway_flag
        }
        for charter in charters
    ]
    return JsonResponse({"results": data, "count": len(data), "term": term})


# Function: Returns an array of Translator objects' properties
def get_translator_data(self):
    translators = []
    if self.request.POST:
        post = self.request.POST
        for key in sorted(post):
            if key.startswith("translator") and key != "translator-count":
                name = post[key] if post[key] else ""
                if name:
                    number = key[10:]
                    docs_signed = True if "docs_signed" + number in post else False
                    translators.append({"name": name, "docs_signed": docs_signed})
    elif self.request.method == "GET":
        if self.object:
            for person in self.object.translators.all():
                translators.append({"name": person.name, "docs_signed": person.docs_signed})
    return translators


# Function: Returns an array of Facilitator objects' properties
def get_facilitator_data(self):
    facilitators = []
    if self.request.POST:
        post = self.request.POST
        for key in sorted(post):
            if key.startswith("facilitator") and key != "facilitator-count":
                name = post[key] if post[key] else ""
                if name:
                    number = key[11:]
                    is_lead = True if "is_lead" + number in post else False
                    speaks_gl = True if "speaks_gl" + number in post else False
                    facilitators.append({"name": name, "is_lead": is_lead, "speaks_gl": speaks_gl})
    elif self.request.method == "GET":
        if self.object:
            for person in self.object.facilitators.all():
                facilitators.append({"name": person.name, "is_lead": person.is_lead, "speaks_gl": person.speaks_gl})
    return facilitators


# Function: Returns an array of Material objects' properties
def get_material_data(self):
    materials = []
    if self.request.POST:
        post = self.request.POST
        for key in sorted(post):
            if key.startswith("material") and key != "material-count":
                name = post[key] if post[key] else ""
                if name:
                    number = key[8:]
                    licensed = True if "licensed" + number in post else False
                    materials.append({"name": name, "licensed": licensed})
    elif self.request.method == "GET":
        if self.object:
            for thing in self.object.materials.all():
                materials.append({"name": thing.name, "licensed": thing.licensed})
    return materials


# Function: Takes an array of translator properties and returns an array of their ids
def get_translator_ids(array):
    ids = []
    for translator in array:
        try:
            person = Translator.objects.get(name=translator["name"])
            person.docs_signed = translator["docs_signed"]
            person.save()
        except Translator.DoesNotExist:
            person = Translator.objects.create(
                name=translator["name"],
                docs_signed=translator["docs_signed"]
            )
        ids.append(person.id)

    return ids


# Function: Takes an array of facilitator properties and returns an array of their ids
def get_facilitator_ids(array):
    ids = []
    for facilitator in array:
        try:
            person = Facilitator.objects.get(name=facilitator["name"])
            person.is_lead = facilitator["is_lead"]
            person.speaks_gl = facilitator["speaks_gl"]
            person.save()
        except Facilitator.DoesNotExist:
            person = Facilitator.objects.create(
                name=facilitator["name"],
                is_lead=facilitator["is_lead"],
                speaks_gl=facilitator["speaks_gl"],
            )
        ids.append(person.id)

    return ids


# Function: Takes an array of material properties and returns an array of their ids
def get_material_ids(array):
    ids = []
    for material in array:
        try:
            object = Material.objects.get(name=material["name"])
            object.licensed = material["licensed"]
            object.save()
        except Material.DoesNotExist:
            object = Material.objects.create(
                name=material["name"],
                licensed=material["licensed"],
            )
        ids.append(object.id)

    return ids


# Function: Takes an instance of Event and returns an array of field names which have
#    the value of "Other"
def check_for_new_items(event):
    fields = []
    if len(event.translation_methods.filter(name="Other")):
        fields.append("translation_methods")
    if len(event.software.filter(name="Other")):
        fields.append("software")
    if len(event.hardware.filter(name="Other")):
        fields.append("hardware")
    if len(event.output_target.filter(name="Other")):
        fields.append("output_target")
    if len(event.publication.filter(name="Other")):
        fields.append("publication")
    return fields


# Function: Takes an instance of Charter and returns the number to be used by the
#    next event for that charter
def get_next_event_number(charter):
    events = Event.objects.filter(charter=charter)
    # TODO: Put in model as model logic
    # event = Event.objects.filter(charter=charter).values("number").order_by("number").first()
    latest = 0
    for event in events:
        if event.number > latest:
            latest = event.number
    return latest + 1
