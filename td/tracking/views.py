import operator

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, TemplateView

from account.mixins import LoginRequiredMixin

from .forms import CharterForm, EventForm
from .models import (
    Charter,
    Event,
    Facilitator,
    Material,
    Translator,
)

from td.utils import DataTableSourceView


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
    link_url_name = "tracking:charter"
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
            "start_date": timezone.now(),
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
        messages.info(self.request, "Project charter has been updated")
        return redirect("tracking:charter_add_success", obj_type="charter", pk=self.object.id)


# -------------------------------------------------------------------
# NOTE: Charter detail will be integrated to the language detail page
# -------------------------------------------------------------------
def charter(request, pk):
    charter = get_object_or_404(Charter, pk=pk)
    messages.info(request, "This page provides a link to edit a charter, but is still being worked on.")
    context = {
        "charter": charter,
    }

    return render(request, "tracking/charter_detail.html", context)


# -------------------------------- #
#            EVENT VIEWS           #
# -------------------------------- #


class EventAddView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm

    # Overwritten to include initial values
    def get_initial(self):
        return {
            "start_date": timezone.now(),
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
        self.object = form.save()

        # Add translators info
        translators = self.get_translator_data(self)
        translator_ids = self.get_translator_ids(translators)
        if translator_ids:
            event = Event.objects.get(pk=self.object.id)
            for id in translator_ids:
                event.translators.add(Translator.objects.get(id=id))

        # Add facilitators info
        facilitators = self.get_facilitator_data(self)
        facilitator_ids = self.get_facilitator_ids(facilitators)
        if facilitator_ids:
            event = Event.objects.get(pk=self.object.id)
            for id in facilitator_ids:
                event.facilitators.add(Facilitator.objects.get(id=id))

        # Add materials info
        materials = self.get_material_data(self)
        material_ids = self.get_material_ids(materials)
        if material_ids:
            event = Event.objects.get(pk=self.object.id)
            for id in material_ids:
                event.materials.add(Material.objects.get(id=id))

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
            "http://localhost:8000/tracking/charter/new/",
            "http://localhost:8000/tracking/event/new/",
            "http://td.unfoldingword.org/tracking/charter/new/",
            "http://td.unfoldingword.org/tracking/event/new/",
        ]

        if referer in allowed_urls:
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
