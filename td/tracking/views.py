import operator
import re
import urlparse

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, TemplateView, DetailView

from account.mixins import LoginRequiredMixin

from .forms import (
    CharterForm,
    EventForm,
    MultiCharterEventForm1,
    MultiCharterEventForm2,
)
from .models import (
    Charter,
    Event,
    Facilitator,
    Material,
    Translator,
)

from td.utils import DataTableSourceView

from django.core.urlresolvers import reverse as urlReverse

from formtools.wizard.views import SessionWizardView


# ------------------------------- #
#            HOME VIEWS           #
# ------------------------------- #


class CharterTableSourceView(DataTableSourceView):

    @property
    def queryset(self):
        if "pk" in self.kwargs:
            return Charter.objects.filter(language=self.kwargs["pk"])
        else:
            return self.model._default_manager.all()

    @property
    def filtered_data(self):
        if len(self.search_term) and len(self.search_term) <= 3:
            qs = self.queryset.filter(
                reduce(
                    operator.or_,
                    [Q(language__name__istartswith=self.search_term)]
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
        if len(self.search_term) and len(self.search_term) <= 3:
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
        "language__code",
        "start_date",
        "end_date",
        "contact_person"
    ]
    # link is on column because name can"t handle non-roman characters
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


# ---------------------------------- #
#            CHARTER VIEWS           #
# ---------------------------------- #


class CharterAdd(LoginRequiredMixin, CreateView):
    model = Charter
    form_class = CharterForm

    # Overwritten to set initial values
    def get_initial(self):
        return {
            "start_date": timezone.now().date(),
            "created_by": self.request.user.username
        }

    # Overwritten to redirect upon valid submission
    def form_valid(self, form):
        self.object = form.save()
        return redirect("tracking:charter_add_success", obj_type="charter", pk=self.object.id)


class CharterUpdate(LoginRequiredMixin, UpdateView):
    model = Charter
    form_class = CharterForm
    template_name_suffix = "_update_form"

    # Overwritten to redirect upon valid submission
    def form_valid(self, form):
        self.object = form.save()
        return redirect("tracking:charter_add_success", obj_type="charter", pk=self.object.id)


# -------------------------------- #
#            EVENT VIEWS           #
# -------------------------------- #


class EventAddView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm

    # Overwritten to include initial values
    def get_initial(self):
        return {
            "start_date": timezone.now().date(),
            "created_by": self.request.user.username,
        }

    # Overwritten to pass URL argument to forms.py
    def get_form_kwargs(self, **kwargs):
        keywords = super(EventAddView, self).get_form_kwargs(**kwargs)
        if "pk" in self.kwargs:
            keywords["pk"] = self.kwargs["pk"]
        return keywords

    # Overwritten to include custom data
    def get_context_data(self, *args, **kwargs):
        context = super(EventAddView, self).get_context_data(**kwargs)
        context["translators"] = self.get_translator_data(self)
        context["facilitators"] = self.get_facilitator_data(self)
        context["materials"] = self.get_material_data(self)
        return context

    # Overwritten to execute custom save and redirect upon valid submission
    def form_valid(self, form):
        event = self.object = form.save()

        # Add translators info
        translators = self.get_translator_data(self)
        translator_ids = self.get_translator_ids(translators)
        event.translators.add(*list(Translator.objects.filter(id__in=translator_ids)))

        # Add facilitators info
        facilitators = self.get_facilitator_data(self)
        facilitator_ids = self.get_facilitator_ids(facilitators)
        event.facilitators.add(*list(Facilitator.objects.filter(id__in=facilitator_ids)))

        # Add materials info
        materials = self.get_material_data(self)
        material_ids = self.get_material_ids(materials)
        event.materials.add(*list(Material.objects.filter(id__in=material_ids)))

        self.set_event_number()

        return redirect("tracking:charter_add_success", obj_type="event", pk=self.object.id)

    # ----------------------------------- #
    #    EVENTADDVIEW CUSTOM FUNCTIONS    #
    # ----------------------------------- #

    # Function: Returns an array of Translator objects' properties
    def get_translator_data(self, form):
        translators = []
        if self.request.POST:
            post = self.request.POST
            for key in sorted(post):
                if key.startswith("translator") and key != "translator-count":
                    name = post[key] if post[key] else ""
                    if name:
                        translators.append({"name": name})
        return translators

    # Function: Returns an array of Facilitator objects' properties
    def get_facilitator_data(self, form):
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
        return facilitators

    # Function: Returns an array of Material objects' properties
    def get_material_data(self, form):
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
        return materials

    # Function: Takes an array of translator properties and returns an array of their ids
    def get_translator_ids(self, array):
        ids = []
        for translator in array:
            try:
                person = Translator.objects.get(name=translator["name"])
            except Translator.DoesNotExist:
                person = Translator.objects.create(name=translator["name"])
            ids.append(person.id)

        return ids

    # Function: Takes an array of facilitator properties and returns an array of their ids
    def get_facilitator_ids(self, array):
        ids = []
        for facilitator in array:
            try:
                person = Facilitator.objects.get(name=facilitator["name"])
            except Facilitator.DoesNotExist:
                person = Facilitator.objects.create(
                    name=facilitator["name"],
                    is_lead=facilitator["is_lead"],
                    speaks_gl=facilitator["speaks_gl"],
                )
            ids.append(person.id)

        return ids

    # Function: Takes an array of material properties and returns an array of their ids
    def get_material_ids(self, array):
        ids = []
        for material in array:
            try:
                object = Material.objects.get(name=material["name"])
            except Material.DoesNotExist:
                object = Material.objects.create(
                    name=material["name"],
                    licensed=material["licensed"],
                )
            ids.append(object.id)

        return ids

    # Function: Sets property:number in event
    def set_event_number(self):
        events = Event.objects.filter(charter=self.object.charter)
        event_numbers = []
        for event in events:
            event_numbers.append(event.number)
        latest = 0
        for number in event_numbers:
            if number > latest:
                latest = number
        Event.objects.filter(pk=self.object.id).update(number=(latest + 1))


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name_suffix = "_update_form"

    # Overwritten to include custom data
    def get_context_data(self, *args, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        context["translators"] = self.get_translator_data(self)
        context["facilitators"] = self.get_facilitator_data(self)
        context["materials"] = self.get_material_data(self)
        return context

    # Overwritten to execute custom save and redirect upon valid submission
    def form_valid(self, form):
        event = self.object = form.save()

        # Update translators info
        translators = self.get_translator_data(self)
        translator_ids = self.get_translator_ids(translators)
        event.translators.clear()
        event.translators.add(*list(Translator.objects.filter(id__in=translator_ids)))

        # Add facilitators info
        facilitators = self.get_facilitator_data(self)
        facilitator_ids = self.get_facilitator_ids(facilitators)
        event.facilitators.clear()
        event.facilitators.add(*list(Facilitator.objects.filter(id__in=facilitator_ids)))

        # Add materials info
        materials = self.get_material_data(self)
        material_ids = self.get_material_ids(materials)
        event.materials.clear()
        event.materials.add(*list(Material.objects.filter(id__in=material_ids)))

        return redirect("tracking:charter_add_success", obj_type="event", pk=self.object.id)

    # ----------------------------------- #
    #    EVENTADDVIEW CUSTOM FUNCTIONS    #
    # ----------------------------------- #

    # Function: Returns an array of Translator objects' properties
    def get_translator_data(self, form):
        translators = []
        if self.request.POST:
            post = self.request.POST
            for key in sorted(post):
                if key.startswith("translator") and key != "translator-count":
                    name = post[key] if post[key] else ""
                    if name:
                        translators.append({"name": name})
        else:
            people = Event.objects.get(pk=self.kwargs["pk"]).translators.all()
            for person in people:
                translators.append({"name": person.name})
        return translators

    # Function: Returns an array of Facilitator objects' properties
    def get_facilitator_data(self, form):
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
        else:
            people = Event.objects.get(pk=self.kwargs["pk"]).facilitators.all()
            for person in people:
                facilitators.append({"name": person.name, "is_lead": person.is_lead, "speaks_gl": person.speaks_gl})
        return facilitators

    # Function: Returns an array of Material objects' properties
    def get_material_data(self, form):
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
        else:
            mats = Event.objects.get(pk=self.kwargs["pk"]).materials.all()
            for mat in mats:
                materials.append({"name": mat.name, "licensed": mat.licensed})
        return materials

    # Function: Takes an array of translator properties and returns an array of their ids
    def get_translator_ids(self, array):
        ids = []
        for translator in array:
            try:
                person = Translator.objects.get(name=translator["name"])
            except Translator.DoesNotExist:
                person = Translator.objects.create(name=translator["name"])
            ids.append(person.id)

        return ids

    # Function: Takes an array of facilitator properties and returns an array of their ids
    def get_facilitator_ids(self, array):
        ids = []
        for facilitator in array:
            try:
                person = Facilitator.objects.get(name=facilitator["name"])
            except Facilitator.DoesNotExist:
                person = Facilitator.objects.create(
                    name=facilitator["name"],
                    is_lead=facilitator["is_lead"],
                    speaks_gl=facilitator["speaks_gl"],
                )
            ids.append(person.id)

        return ids

    # Function: Takes an array of material properties and returns an array of their ids
    def get_material_ids(self, array):
        ids = []
        for material in array:
            try:
                object = Material.objects.get(name=material["name"])
            except Material.DoesNotExist:
                object = Material.objects.create(
                    name=material["name"],
                    licensed=material["licensed"],
                )
            ids.append(object.id)

        return ids


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        context["event"] = self.object
        return context


# -------------------------------- #
#            OTHER VIEWS           #
# -------------------------------- #


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
            context["message"] = "Project " + charter.language.name + " has been successfully added."
        elif kwargs["obj_type"] == "event":
            event = Event.objects.get(pk=kwargs["pk"])
            context["message"] = "Your event for " + event.charter.language.name + " has been successfully added."
        else:
            context["status"] = "Sorry :("
            context["message"] = "It seems like you got here by accident"
        return context


class MultiCharterEventView(LoginRequiredMixin, SessionWizardView):
    template_name = 'tracking/multi_charter_event_form.html'
    form_list = [MultiCharterEventForm1, MultiCharterEventForm2]
    success_url = '/success/'

    def done(self, form_list, form_dict, **kwargs):
        print 'FORM LIST', form_list
        print 'FORM DICT', form_dict
        print 'KWARGS', kwargs
        return HttpResponseRedirect('/success/')


class NewCharterModalView(CharterAdd):

    template_name = 'tracking/new_charter_modal.html'

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, "tracking/new_charter_modal.html", {"success": True})


# -------------------- #
#    VIEW FUNCTIONS    #
# -------------------- #


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
