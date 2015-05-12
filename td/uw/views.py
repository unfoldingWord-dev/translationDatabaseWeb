from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.db.models import Q
from django.contrib import messages

from account.decorators import login_required
from account.mixins import LoginRequiredMixin
from eventlog.models import log
from .tasks import get_map_gateways

import operator

from .forms import (
    CountryForm,
    LanguageForm,
    NetworkForm,
    ResourceForm,
    UploadGatewayForm,
)
from .models import (
    Country,
    Language,
    Network,
    Resource,
    transform_country_data,
    Region,
)

from td.utils import DataTableSourceView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "uw/home.html"


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
    if request.method == "POST":
        form = UploadGatewayForm(request.POST, request.FILES)
        if form.is_valid():
            for lang in Language.objects.filter(code__in=form.cleaned_data["languages"]):
                lang.gateway_flag = True
                lang.source = request.user
                lang.save()
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
    return render(request, "uw/gateway_languages_update.html", {"form": form})


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
    return render(request, "uw/rtl_languages_update.html", {"form": form})


class EntityTrackingMixin(object):

    def get_form_kwargs(self):
        kwargs = super(EntityTrackingMixin, self).get_form_kwargs()
        kwargs.update({
            "source": self.request.user
        })
        return kwargs


class EventLogMixin(object):

    @property
    def action(self):
        return "{}_{}".format(
            self.action_kind,
            self.model._meta.verbose_name.upper().replace(" ", "_")
        )

    @property
    def extra_data(self):
        data = {
            "pk": self.object.pk
        }
        return data

    @property
    def user(self):
        if self.request.user.is_authenticated():
            return self.request.user
        return None

    def log_action(self):
        log(
            user=self.user,
            action=self.action,
            extra=self.extra_data
        )

    def form_valid(self, form):
        response = super(EventLogMixin, self).form_valid(form)
        self.log_action()
        return response


class RegionListView(ListView):
    model = Region
    template_name = "uw/region_list.html"

    def get_queryset(self):
        return Region.objects.all()


class RegionDetailView(ListView):
    model = Region
    template_name = "uw/region_detail.html"

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

    def get_queryset(self):
        qs = super(CountryListView, self).get_queryset()
        qs = qs.order_by("name")
        return qs


class CountryDetailView(DetailView):
    model = Country


class CountryEditView(LoginRequiredMixin, EventLogMixin, EntityTrackingMixin, UpdateView):
    model = Country
    form_class = CountryForm
    action_kind = "EDIT"

    def get_success_url(self):
        return reverse("country_detail", args=[self.object.pk])


class LanguageTableSourceView(DataTableSourceView):

    def __init__(self, **kwargs):
        super(LanguageTableSourceView, self).__init__(**kwargs)

    @property
    def queryset(self):
        if "pk" in self.kwargs:
            return Language.objects.filter(gateway_language=self.kwargs["pk"])
        else:
            return self.model._default_manager.all()

    @property
    def filtered_data(self):
        if len(self.search_term) and len(self.search_term) <= 3:
            qs = self.queryset.filter(
                reduce(
                    operator.or_,
                    [Q(code__istartswith=self.search_term)]
                )
            ).order_by("code")
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


class LanguageListView(TemplateView):
    template_name = "uw/language_list.html"


class AjaxLanguageListView(LanguageTableSourceView):
    model = Language
    fields = [
        "code",
        "iso_639_3",
        "name",
        "direction",
        "country__name",
        "native_speakers",
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
        "direction",
        "country__name",
        "native_speakers",
        "gateway_flag"
    ]
    link_column = "code"
    link_url_name = "language_detail"
    link_url_field = "pk"


class LanguageCreateView(LoginRequiredMixin, EventLogMixin, EntityTrackingMixin, CreateView):
    model = Language
    form_class = LanguageForm
    action_kind = "CREATE"

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

    def get_context_data(self, **kwargs):
        context = super(LanguageDetailView, self).get_context_data(**kwargs)
        context.update({
            "country": self.object.country
        })
        return context


class LanguageEditView(LoginRequiredMixin, EventLogMixin, EntityTrackingMixin, UpdateView):
    model = Language
    form_class = LanguageForm
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


class NetworkEditView(LoginRequiredMixin, EventLogMixin, EntityTrackingMixin, UpdateView):
    model = Network
    form_class = NetworkForm
    action_kind = "EDIT"

    def get_success_url(self):
        return reverse("network_detail", args=[self.object.pk])


class NetworkListView(ListView):
    model = Network

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


class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm
    action_kind = "CREATE"

    def dispatch(self, request, *args, **kwargs):
        self.language = get_object_or_404(Language, pk=self.kwargs.get("pk"))
        return super(ResourceCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.language = self.language
        self.object.save()
        return redirect("language_detail", self.language.pk)

    def get_context_data(self, **kwargs):
        context = super(ResourceCreateView, self).get_context_data(**kwargs)
        context.update({
            "language": self.language
        })
        return context


class ResourceEditView(LoginRequiredMixin, UpdateView):
    model = Resource
    form_class = ResourceForm
    action_kind = "EDIT"

    def get_success_url(self):
        return reverse("language_detail", self.object.language.pk)

    def get_context_data(self, **kwargs):
        context = super(ResourceEditView, self).get_context_data(**kwargs)
        context.update({
            "language": self.object.language,
        })
        return context
