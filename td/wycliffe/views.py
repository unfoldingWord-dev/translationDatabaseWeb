from django.views.generic import ListView, CreateView, UpdateView, DetailView

from account.mixins import LoginRequiredMixin

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


class CountryCreateView(LoginRequiredMixin, CreateView):
    model = Country


class CountryDetailView(LoginRequiredMixin, DetailView):
    model = Country


class CountryEditView(LoginRequiredMixin, UpdateView):
    model = Country


class LanguageListView(LoginRequiredMixin, ListView):
    model = Language


class LanguageCreateView(LoginRequiredMixin, CreateView):
    model = Language


class LanguageDetailView(LoginRequiredMixin, DetailView):
    model = Language


class LanguageEditView(LoginRequiredMixin, UpdateView):
    model = Language


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
