from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from account.mixins import LoginRequiredMixin

from .forms import (
    CountryForm,
    LanguageForm
)
from .models import (
    Country,
    Language,
    WorkInProgress,
    Scripture,
    TranslationNeed,
    Resource
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


class WIPListView(LoginRequiredMixin, ListView):
    model = WorkInProgress


class WIPCreateView(LoginRequiredMixin, CreateView):
    model = WorkInProgress


class ScriptureListView(LoginRequiredMixin, ListView):
    model = Scripture


class ScriptureCreateView(LoginRequiredMixin, CreateView):
    model = Scripture


class TranslationNeedListView(LoginRequiredMixin, ListView):
    model = TranslationNeed


class TranslationNeedCreateView(LoginRequiredMixin, CreateView):
    model = TranslationNeed


class ResourceListView(LoginRequiredMixin, ListView):
    model = Resource


class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource


class WIPEditView(LoginRequiredMixin, UpdateView):
    model = WorkInProgress


class ScriptureEditView(LoginRequiredMixin, UpdateView):
    model = Scripture


class TranslationNeedEditView(LoginRequiredMixin, UpdateView):
    model = TranslationNeed


class ResourceEditView(LoginRequiredMixin, UpdateView):
    model = Resource
