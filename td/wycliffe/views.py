from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from account.mixins import LoginRequiredMixin

from .forms import (
    CountryForm,
    LanguageForm,
    ResourceForm,
    ScriptureForm,
    TranslationNeedForm,
    WorkInProgressForm
)
from .models import (
    Country,
    Language,
    Resource,
    Scripture,
    TranslationNeed,
    WorkInProgress
)


class CountryListView(LoginRequiredMixin, ListView):
    model = Country

    def get_queryset(self):
        qs = super(CountryListView, self).get_queryset()
        qs = qs.order_by("country__name")
        return qs


class CountryDetailView(LoginRequiredMixin, DetailView):
    model = Country


class CountryEditView(LoginRequiredMixin, UpdateView):
    model = Country
    form_class = CountryForm

    def get_success_url(self):
        return reverse("country_detail", args=[self.object.pk])


class LanguageCreateView(LoginRequiredMixin, CreateView):
    model = Language
    form_class = LanguageForm

    def dispatch(self, request, *args, **kwargs):
        self.country = get_object_or_404(Country, pk=self.kwargs.get("pk"))
        return super(LanguageCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        language = form.save(commit=False)
        language.country = self.country
        language.save()
        form.save_m2m()
        return redirect("language_detail", language.pk)

    def get_context_data(self, **kwargs):
        context = super(LanguageCreateView, self).get_context_data(**kwargs)
        context.update({
            "country": self.country
        })
        return context


class LanguageDetailView(LoginRequiredMixin, DetailView):
    model = Language


class LanguageEditView(LoginRequiredMixin, UpdateView):
    model = Language
    form_class = LanguageForm

    def get_success_url(self):
        return reverse("language_detail", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super(LanguageEditView, self).get_context_data(**kwargs)
        context.update({
            "country": self.object.country
        })
        return context


class BaseLanguageView(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        self.language = get_object_or_404(Language, pk=self.kwargs.get("pk"))
        return super(BaseLanguageView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.language = self.language
        obj.save()
        form.save_m2m()
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


class ScriptureCreateView(BaseLanguageView, CreateView):
    model = Scripture
    form_class = ScriptureForm


class TranslationNeedCreateView(BaseLanguageView, CreateView):
    model = TranslationNeed
    form_class = TranslationNeedForm


class ResourceCreateView(BaseLanguageView, CreateView):
    model = Resource
    form_class = ResourceForm


class WIPEditView(BaseLanguageView, UpdateView):
    model = WorkInProgress
    form_class = WorkInProgressForm


class ScriptureEditView(BaseLanguageView, UpdateView):
    model = Scripture
    form_class = ScriptureForm


class TranslationNeedEditView(BaseLanguageView, UpdateView):
    model = TranslationNeed
    form_class = TranslationNeedForm


class ResourceEditView(BaseLanguageView, UpdateView):
    model = Resource
    form_class = ResourceForm
