from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView

from account.decorators import login_required
from account.mixins import LoginRequiredMixin
from eventlog.models import log

from .forms import (
    CountryForm,
    LanguageForm,
    NetworkForm,
    ResourceForm,
)
from .models import (
    Country,
    Language,
    Network,
    Resource,
    transform_country_data,
    Region,
)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "uw/home.html"


@login_required
def country_tree_data(request):
    return JsonResponse(transform_country_data(Country.gateway_data()))


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


class RegionListView(LoginRequiredMixin, ListView):
    model = Region
    template_name = "uw/region_list.html"

    def get_queryset(self):
        return Region.objects.all()


class RegionDetailView(LoginRequiredMixin, ListView):
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


class CountryListView(LoginRequiredMixin, ListView):
    model = Country

    def get_queryset(self):
        qs = super(CountryListView, self).get_queryset()
        qs = qs.order_by("name")
        return qs


class CountryDetailView(LoginRequiredMixin, DetailView):
    model = Country


class CountryEditView(LoginRequiredMixin, EventLogMixin, EntityTrackingMixin, UpdateView):
    model = Country
    form_class = CountryForm
    action_kind = "EDIT"

    def get_success_url(self):
        return reverse("country_detail", args=[self.object.pk])


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


class LanguageDetailView(LoginRequiredMixin, DetailView):
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


class NetworkDetailView(LoginRequiredMixin, DetailView):
    model = Network


class NetworkEditView(LoginRequiredMixin, EventLogMixin, EntityTrackingMixin, UpdateView):
    model = Network
    form_class = NetworkForm
    action_kind = "EDIT"

    def get_success_url(self):
        return reverse("network_detail", args=[self.object.pk])


class NetworkListView(LoginRequiredMixin, ListView):
    model = Network

    def get_queryset(self):
        qs = super(NetworkListView, self).get_queryset()
        qs = qs.order_by("name")
        return qs


class ContentView(LoginRequiredMixin, ListView):
    model = Content



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


class WIPCreateView(BaseLanguageView, CreateView):
    model = WorkInProgress
    form_class = WorkInProgressForm
    action_kind = "CREATE"

    def get_context_data(self, **kwargs):
        context = super(WIPCreateView, self).get_context_data(**kwargs)
        context.update({
            "country": self.language.country
        })
        return context


class ScriptureCreateView(BaseLanguageView, CreateView):
    model = Scripture
    form_class = ScriptureForm
    action_kind = "CREATE"

    def get_context_data(self, **kwargs):
        context = super(ScriptureCreateView, self).get_context_data(**kwargs)
        context.update({
            "country": self.language.country
        })
        return context

    def get_form_kwargs(self):
        kwargs = super(ScriptureCreateView, self).get_form_kwargs()
        kwargs.update({
            "language": self.language
        })
        return kwargs


class TranslationNeedCreateView(BaseLanguageView, CreateView):
    model = TranslationNeed
    form_class = TranslationNeedForm
    action_kind = "CREATE"

    def get_context_data(self, **kwargs):
        context = super(TranslationNeedCreateView, self).get_context_data(**kwargs)
        context.update({
            "country": self.language.country
        })
        return context


class ResourceCreateView(BaseLanguageView, CreateView):
    model = Resource
    form_class = ResourceForm
    action_kind = "CREATE"

    def get_context_data(self, **kwargs):
        context = super(ResourceCreateView, self).get_context_data(**kwargs)
        context.update({
            "country": self.language.country
        })
        return context


class WIPEditView(BaseLanguageView, UpdateView):
    model = WorkInProgress
    form_class = WorkInProgressForm
    action_kind = "EDIT"

    def get_context_data(self, **kwargs):
        context = super(WIPEditView, self).get_context_data(**kwargs)
        context.update({
            "country": self.language.country
        })
        return context


class ScriptureEditView(BaseLanguageView, UpdateView):
    model = Scripture
    form_class = ScriptureForm
    action_kind = "EDIT"

    def get_context_data(self, **kwargs):
        context = super(ScriptureEditView, self).get_context_data(**kwargs)
        context.update({
            "country": self.language.country
        })
        return context

    def get_form_kwargs(self):
        kwargs = super(ScriptureEditView, self).get_form_kwargs()
        kwargs.update({
            "language": self.language
        })
        return kwargs


class TranslationNeedEditView(BaseLanguageView, UpdateView):
    model = TranslationNeed
    form_class = TranslationNeedForm
    action_kind = "EDIT"


class ResourceEditView(BaseLanguageView, UpdateView):
    model = Resource
    form_class = ResourceForm
    action_kind = "EDIT"
