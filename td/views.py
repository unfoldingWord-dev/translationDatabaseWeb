import requests
import uuid
import time
import hashlib

from account.decorators import login_required
from account.mixins import LoginRequiredMixin
from pinax.eventlog.mixins import EventLogMixin
from formtools.wizard.views import SessionWizardView
from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView, UpdateView, CreateView
from django.views.decorators.csrf import csrf_exempt

from .imports.models import (
    EthnologueCountryCode,
    EthnologueLanguageCode,
    EthnologueLanguageIndex,
    SIL_ISO_639_3,
    WikipediaISOLanguage,
    IMBPeopleGroup
)
from .tracking.models import Event
from .models import Language, Country, Region, Network, AdditionalLanguage, JSONData, WARegion, TempLanguage
from .forms import NetworkForm, CountryForm, LanguageForm, UploadGatewayForm, TempLanguageForm
from .resources.models import transform_country_data, Questionnaire
from .resources.tasks import get_map_gateways
from .resources.views import EntityTrackingMixin
from .tasks import reset_langnames_cache
from .utils import DataTableSourceView, svg_to_pdf


def codes_text_export(request):
    return HttpResponse(Language.codes_text(), content_type="text/plain")


def names_text_export(request):
    return HttpResponse(Language.names_text(), content_type="text/plain")


def names_json_export(request):
    # NOTE: Temp solution to langnames.json caching problem
    # NOTE: This is the caching way
    # data = get_langnames()
    # NOTE: This is the direct, snychronous way
    # data = Language.names_data()
    # NOTE: This is the DB/management command way
    langnames = JSONData.objects.get(name="langnames")
    # Set safe to False to allow list instead of dict to be returned
    return JsonResponse(langnames.data, safe=False)


@csrf_exempt
def export_svg(request):
    svg = request.POST.get("data")
    response = HttpResponse(content_type="application/pdf")
    response.write(svg_to_pdf(svg))
    response["Content-Disposition"] = "attachment; filename=gateway_languages_map.pdf"
    return response


def cache_get_or_set(key, acallable):
    data = cache.get(key)
    if data is None:
        data = acallable()
        cache.set(key, data, None)
    return data


def get_langnames(short=False):
    key = "langnames_short" if short else "langnames"
    fetching = "_".join([key, "fetching"])
    data = cache.get(key, [])
    if not data and cache.get(fetching, False) is False:
        reset_langnames_cache.delay(short=short)
    return data


def languages_autocomplete(request):
    term = request.GET.get("q").lower()
    data = get_langnames(short=True)
    d = []
    if len(term) <= 3:
        term = term.encode("utf-8")
        # search: lc
        # first do a *starts with* style search of language code (lc)
        d.extend([
            x
            for x in data
            if term == x["lc"].lower()[:len(term)]
        ])
    if len(term) >= 3:
        # search: lc, ln, lr
        term = term.encode("utf-8")
        d.extend([
            x
            for x in data
            if (
                term in x["lc"] or term in x["ln"].lower() or
                term in x["ang"].lower() or term in x["lr"].lower()
            )
        ])
    return JsonResponse({"results": d, "count": len(d), "term": term})


class AdditionalLanguageListView(TemplateView):
    template_name = "td/additionallanguage_list.html"


class EthnologueCountryCodeListView(TemplateView):
    template_name = "td/ethnologuecountrycode_list.html"


class EthnologueLanguageCodeListView(TemplateView):
    template_name = "td/ethnologuelanguagecode_list.html"


class EthnologueLanguageIndexListView(TemplateView):
    template_name = "td/ethnologuelanguageindex_list.html"


class SIL_ISO_639_3ListView(TemplateView):
    template_name = "td/sil_list.html"


class WikipediaISOLanguageListView(TemplateView):
    template_name = "td/wikipedia_list.html"


class IMBPeopleGroupListView(TemplateView):
    template_name = "td/imbpeoplegroup_list.html"


class AjaxAdditionalLanguageListView(DataTableSourceView):
    model = AdditionalLanguage
    fields = [
        "ietf_tag",
        "two_letter",
        "three_letter",
        "common_name",
        "native_name",
        "direction",
        "comment"
    ]


class AjaxEthnologueCountryCodeListView(DataTableSourceView):
    model = EthnologueCountryCode
    fields = [
        "code",
        "name",
        "area"
    ]


class AjaxEthnologueLanguageCodeListView(DataTableSourceView):
    model = EthnologueLanguageCode
    fields = [
        "code",
        "country_code",
        "status",
        "name"
    ]


class AjaxEthnologueLanguageIndexListView(DataTableSourceView):
    model = EthnologueLanguageIndex
    fields = [
        "language_code",
        "country_code",
        "name_type",
        "name"
    ]


class AjaxSIL_ISO_639_3ListView(DataTableSourceView):
    model = SIL_ISO_639_3
    fields = [
        "code",
        "part_2b",
        "part_2t",
        "part_1",
        "scope",
        "language_type",
        "ref_name",
        "comment"
    ]


class AjaxWikipediaISOLanguageListView(DataTableSourceView):
    model = WikipediaISOLanguage
    fields = [
        "language_family",
        "language_name",
        "native_name",
        "iso_639_1",
        "iso_639_2t",
        "iso_639_2b",
        "iso_639_3",
        "iso_639_9",
        "notes"
    ]


class AjaxIMBPeopleGroupListView(DataTableSourceView):
    model = IMBPeopleGroup
    fields = [
        "peid",
        "affinity_bloc",
        "people_cluster",
        "sub_continent",
        "country",
        "country_of_origin",
        "people_group",
        "population",
        "dispersed",
        "rol",
        "language",
        "religion",
        "written_scripture",
        "jesus_film",
        "radio_broadcast",
        "gospel_recording",
        "audio_scripture",
        "bible_stories"
    ]


@login_required
def country_tree_data(request):
    return JsonResponse(transform_country_data(Country.gateway_data()))


def country_map_data(request):
    language_to_color = {
        "defaultFill": "#CCCCCC",
        "en": "#ACEA73",
        "fr": "#CCAAEA",
        "es": "#E9E36F",
        "es-419": "#E9E36F",
        "pt": "#E1AB5B",
        "nl": "#BA4759",
        "hi": "#868686",
        "ru": "#794C53",
        "ar": "#84E9CF",
        "sw": "#F54982",
        "am": "#F7E718",
        "tr": "#3A39DD",
        "ps": "#6FCF1A",
        "ja": "#216A8B",
        "id": "#591468",
        "zh": "#6B9BE0",
        "km": "#39FF06",
        "tl": "#DEE874",
        "bn": "#346507",
        "my": "#F1FF31",
        "lo": "#CE0008",
        "th": "#B7FFF8",
        "mn": "#DE7E6A",
        "fa": "#5F441A",
        "ur": "#BEB41F",
        "vi": "#E8AB50",
        "ne": "#741633",
        "dz": "#F2951C",
        "ms": "#A7DA3D",
        "pis": "#8A8A8A",
        "tpi": "#E966C7",
        "ta": "#8A8A8A"
    }
    map_gateways = get_map_gateways()
    return JsonResponse({"fills": language_to_color, "country_data": map_gateways})


@login_required
def upload_gateway_flag_file(request):
    """ Flag each language matching the language code in a newline-delimited list of codes as "gateway" languages.
    Unflag any languages which were previously marked as "gateway" languages but are not submitted in the form.
    """
    if request.method == "POST":
        form = UploadGatewayForm(request.POST, request.FILES)
        if form.is_valid():
            Language.objects.filter(gateway_flag=True).update(gateway_flag=False)
            Language.objects.filter(code__in=form.cleaned_data["languages"]).update(gateway_flag=True)
            messages.add_message(request, messages.SUCCESS, "Gateway languages updated")
            return redirect("gateway_flag_update")
    else:
        form = UploadGatewayForm(
            initial={
                "languages": "\n".join([
                    l.code.lower()
                    for l in Language.objects.filter(gateway_flag=True).order_by("code")
                ])
            }
        )
    return render(request, "resources/gateway_languages_update.html", {"form": form})


@login_required
def upload_rtl_list(request):
    if request.method == "POST":
        form = UploadGatewayForm(request.POST)
        if form.is_valid():
            for lang in Language.objects.filter(code__in=form.cleaned_data["languages"]):
                lang.direction = "r"
                lang.source = request.user
                lang.save()
            messages.add_message(request, messages.SUCCESS, "RTL languages updated")
            return redirect("rtl_languages_update")
    else:
        form = UploadGatewayForm(
            initial={
                "languages": "\n".join([
                    l.code.lower()
                    for l in Language.objects.filter(direction="r").order_by("code")
                ])
            }
        )
    return render(request, "resources/rtl_languages_update.html", {"form": form})


class RegionListView(ListView):
    model = Region
    template_name = "resources/region_list.html"

    def get_queryset(self):
        return Region.objects.all()


class RegionDetailView(ListView):
    model = Region
    template_name = "resources/region_detail.html"

    def get_context_data(self, **kwargs):
        region = Region.objects.get(slug=self.kwargs.get("slug"))
        context = super(RegionDetailView, self).get_context_data(**kwargs)
        context.update({
            "region": region,
            "country_list": region.countries.all(),
            "languages": Language.objects.filter(country__region=region).order_by("name")
        })
        return context

    def get_queryset(self):
        qs = super(RegionDetailView, self).get_queryset()
        qs = qs.filter(slug__iexact=self.kwargs.get("slug"))
        qs = qs.order_by("name")
        return qs


class CountryListView(ListView):
    model = Country
    template_name = "resources/country_list.html"

    def get_queryset(self):
        qs = super(CountryListView, self).get_queryset()
        qs = qs.order_by("name")
        return qs


class CountryDetailView(DetailView):
    model = Country
    template_name = "resources/country_detail.html"


class CountryEditView(LoginRequiredMixin, EventLogMixin, EntityTrackingMixin, UpdateView):
    model = Country
    form_class = CountryForm
    action_kind = "EDIT"
    template_name = "resources/country_form.html"

    def get_success_url(self):
        return reverse("country_detail", args=[self.object.pk])


class LanguageTableSourceView(DataTableSourceView):

    @property
    def queryset(self):
        if "pk" in self.kwargs:
            return Language.objects.filter(gateway_language=self.kwargs["pk"])
        else:
            return self.model.objects.all()

    @property
    def filtered_data(self):
        """
        Return results of the language code filtered by search_term if the
        search_term is 3 or less characters long, otherwise defer to inherited
        behavior.
        """
        search_term = self.search_term.strip()
        if search_term and len(search_term) <= 1:
            qs = self.queryset.filter(code__startswith=search_term.lower())
            if qs.count():
                return qs.order_by("code")

        return super(LanguageTableSourceView, self).filtered_data


class TempLanguageTableSourceView(DataTableSourceView):

    @property
    def queryset(self):
        if "pk" in self.kwargs:
            return Language.objects.filter(gateway_language=self.kwargs["pk"])
        else:
            return self.model.objects.all()


class CountryTableSourceView(DataTableSourceView):

    @property
    def queryset(self):
        if "pk" in self.kwargs:
            return Country.objects.filter(gateway_language=self.kwargs["pk"])
        elif "slug" in self.kwargs:
            return Country.objects.filter(wa_region__slug=self.kwargs["slug"])
        else:
            return self.model._default_manager.all()


class AjaxCountryListView(CountryTableSourceView):
    model = Country
    fields = [
        "code",
        "alpha_3_code",
        "name",
        "region__name",
        "wa_region__name",
        "population",
    ]
    link_column = "name"
    link_url_name = "country_detail"
    link_url_field = "pk"


class LanguageListView(TemplateView):
    template_name = "resources/language_list.html"

    def get_context_data(self, **kwargs):
        context = super(LanguageListView, self).get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class AjaxLanguageListView(LanguageTableSourceView):
    model = Language
    fields = [
        "code",
        "iso_639_3",
        "name",
        "alt_names",
        "anglicized_name",
        "country__name",
        "gateway_language__name",
        "gateway_flag"
    ]
    link_column = "code"
    link_url_name = "language_detail"
    link_url_field = "pk"


class AjaxLanguageGatewayListView(LanguageTableSourceView):
    model = Language
    fields = [
        "code",
        "iso_639_3",
        "name",
        "anglicized_name",
        "alt_names",
        "country__name",
        "native_speakers",
    ]
    link_column = "code"
    link_url_name = "language_detail"
    link_url_field = "pk"


class LanguageCreateView(LoginRequiredMixin, EventLogMixin, EntityTrackingMixin, CreateView):
    model = Language
    form_class = LanguageForm
    action_kind = "CREATE"
    # Removed the following because we don't want user to create additional language on their own
    # template_name = "resources/language_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.country = get_object_or_404(Country, pk=self.kwargs.get("pk"))
        return super(LanguageCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.country = self.country
        self.object.save()
        form.save_m2m()
        self.log_action()
        return redirect("language_detail", self.object.pk)

    def get_context_data(self, **kwargs):
        context = super(LanguageCreateView, self).get_context_data(**kwargs)
        context.update({
            "country": self.country
        })
        return context


class LanguageDetailView(DetailView):
    model = Language
    template_name = "resources/language_detail.html"

    def get_context_data(self, **kwargs):
        context = super(LanguageDetailView, self).get_context_data(**kwargs)
        jp_resp = requests.get('http://joshuaproject.net/api/v2/languages', {
            'api_key': settings.JP_API_KEY,
            'ROL3': self.object.iso_639_3,
        })
        jp_status_code = jp_resp.json()['status']['status_code']
        context.update({
            "country": self.object.country,
            "countries": [Country.objects.get(code=c).name
                          for c in self.object.cc_all],
            "jp_status_code": str(jp_status_code),
            "jp": jp_resp.json()['data'][0] if jp_status_code == 200 else None,
        })
        # For translation project integration
        # ---------------------------------------------------------
        try:
            charter = self.object.charter
            events = Event.objects.filter(charter=charter.id)
            context.update({"charter": charter, "events": events})
        except ObjectDoesNotExist:
            # It shold be fine to let this pass because the template will not print anything
            #    if no charter or event is passed.
            pass
        # ---------------------------------------------------------
        return context


class LanguageEditView(LoginRequiredMixin, EventLogMixin, EntityTrackingMixin, UpdateView):
    model = Language
    form_class = LanguageForm
    template_name = "resources/language_form.html"
    action_kind = "EDIT"

    def get_success_url(self):
        return reverse("language_detail", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super(LanguageEditView, self).get_context_data(**kwargs)
        context.update({
            "country": self.object.country
        })
        return context


class NetworkCreateView(LoginRequiredMixin, EventLogMixin, EntityTrackingMixin, CreateView):
    model = Network
    form_class = NetworkForm
    action_kind = "CREATE"

    def get_success_url(self):
        return reverse("network_detail", args=[self.object.pk])


class NetworkDetailView(DetailView):
    model = Network
    template_name = "resources/network_detail.html"


class NetworkEditView(LoginRequiredMixin, EventLogMixin, EntityTrackingMixin, UpdateView):
    model = Network
    form_class = NetworkForm
    action_kind = "EDIT"
    template_name = "resources/network_form.html"

    def get_success_url(self):
        return reverse("network_detail", args=[self.object.pk])


class NetworkListView(ListView):
    model = Network
    template_name = "resources/network_list.html"

    def get_queryset(self):
        qs = super(NetworkListView, self).get_queryset()
        qs = qs.order_by("name")
        return qs


class BaseLanguageView(LoginRequiredMixin, EventLogMixin, EntityTrackingMixin):

    def dispatch(self, request, *args, **kwargs):
        self.language = get_object_or_404(Language, pk=self.kwargs.get("pk"))
        return super(BaseLanguageView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.language = self.language
        self.object.save()
        form.save_m2m()
        self.log_action()
        return redirect("language_detail", self.language.pk)

    def get_context_data(self, **kwargs):
        context = super(BaseLanguageView, self).get_context_data(**kwargs)
        context.update({
            "language": self.language
        })
        return context


class WARegionListView(LoginRequiredMixin, ListView):
    model = WARegion
    context_object_name = "wa_regions"
    template_name = "resources/waregion_list.html"


class WARegionDetailView(LoginRequiredMixin, DetailView):
    model = WARegion
    context_object_name = "wa_region"
    template_name = "resources/waregion_detail.html"

    def get_context_data(self, **kwargs):
        wa_region = self.get_object()
        context = super(WARegionDetailView, self).get_context_data(**kwargs)
        context["gl_directors"] = wa_region.gldirector_set.filter(is_helper=False)
        context["gl_helpers"] = wa_region.gldirector_set.filter(is_helper=True)
        return context


class TempLanguageListView(LoginRequiredMixin, ListView):
    model = TempLanguage
    template_name = "resources/templanguage_list.html"


class TempLanguageDetailView(LoginRequiredMixin, DetailView):
    model = TempLanguage
    template_name = "resources/templanguage_detail.html"


class TempLanguageWizardView(LoginRequiredMixin, SessionWizardView):
    # form_list is defined here because WizardView demands it. It will be replaced by the actual form that we'll create
    #    in get_form_list()
    form_list = [forms.Form]
    template_name = "resources/templanguage_wizard_form.html"

    def get_form_list(self):
        # Update form_list with dynamically-created forms based on the questions in the latest questionnaire
        grouped_questions = Questionnaire.objects.latest('created_at').grouped_questions
        step = 0
        for group in grouped_questions:
            fields = {}
            for question in group:
                label = question["text"]
                help_text = question["help"]
                required = question["required"]
                widget_attrs = {"class": str(required), "required": required, "autofocus": "true"}
                if question["input_type"] == "boolean":
                    field = forms.ChoiceField(label=label, help_text=help_text, required=required,
                                              choices=(("", ""), ("Yes", "Yes"), ("No", "No")),
                                              widget=forms.Select(attrs=widget_attrs))
                else:
                    field = forms.CharField(label=label, help_text=help_text, required=required,
                                            widget=forms.TextInput(attrs=widget_attrs))
                fields.update({"question-" + str(question["id"]): field})
            new_form = type("NewForm" + str(step), (forms.Form, ), fields)
            self.form_list.update({unicode(step): new_form})
            step += 1
        # At the end, add TempLanguageForm that contains temp code generator
        self.form_list.update({unicode(step): TempLanguageForm})
        return self.form_list

    def done(self, form_list, **kwargs):
        data = self.get_all_cleaned_data()
        user = self.request.user
        answers = [{"text": value, "question_id": key.split("-")[1]}
                   for key, value in data.iteritems() if key.startswith("question-")]
        obj = TempLanguage(request_id=uuid.uuid1(), app="td", answers=answers, created_by=user, modified_by=user,
                           code=data["code"], questionnaire=data["questionnaire"],
                           requester=(user.first_name + " " + user.last_name).strip() or user.username)
        obj.save()
        return redirect(obj.lang_assigned_url)


class TempLanguageUpdateView(LoginRequiredMixin, UpdateView):
    model = TempLanguage
    form_class = TempLanguageForm
    template_name = "resources/templanguage_form.html"

    def get_context_data(self, **kwargs):
        context = super(TempLanguageUpdateView, self).get_context_data(**kwargs)
        # Manually passing ietf_tag along because the form input was rendered manually
        context["code"] = self.request.POST.get("code", "")
        context["edit"] = True
        return context

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super(TempLanguageUpdateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class AjaxTempLanguageListView(TempLanguageTableSourceView):
    model = TempLanguage
    fields = [
        "code",
        "lang_assigned__name",
        "status",
        "app",
        "requester",
    ]
    link_column = "code"
    link_url_name = "templanguage_detail"
    link_url_field = "pk"


class AjaxTemporaryCode(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.generate_temp_code())

    def generate_temp_code(self):
        """
        Generate a temporary language code from UUID and Time Since Epoch
        :return: A code with "qaa-x-" and the first 6 letters of the hash
        """
        stamp = "".join([str(uuid.uuid1()), str(time.time())])
        stamp_hash = hashlib.sha1(stamp).hexdigest()
        temp_code = "-".join(["qaa", "x", stamp_hash[:6]])
        try:
            TempLanguage.objects.get(code=temp_code)
            return self.generate_temp_code()
        except TempLanguage.DoesNotExist:
            return temp_code


class TempLanguageAdminView(LoginRequiredMixin, TemplateView):
    template_name = "resources/templanguage_admin.html"
