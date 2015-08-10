from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from account.mixins import LoginRequiredMixin

from pinax.eventlog.mixins import EventLogMixin
from .forms import (
    ResourceForm,
    TitleForm,
    PublisherForm
)
from .models import (
    Resource,
    Title,
    Publisher
)
from td.models import Language


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "resources/home.html"


class EntityTrackingMixin(object):

    def get_form_kwargs(self):
        kwargs = super(EntityTrackingMixin, self).get_form_kwargs()
        kwargs.update({
            "source": self.request.user
        })
        return kwargs


class PublisherListView(ListView):
    model = Publisher

    def get_queryset(self):
        qs = super(PublisherListView, self).get_queryset()
        qs = qs.order_by("name")
        return qs


class PublisherDetailView(DetailView):
    model = Publisher


class PublisherEditView(LoginRequiredMixin, EventLogMixin, UpdateView):
    model = Publisher
    form_class = PublisherForm
    action_kind = "EDIT"

    def get_success_url(self):
        return reverse("publisher_detail", args=[self.object.pk])


class PublisherCreateView(LoginRequiredMixin, EventLogMixin, CreateView):
    model = Publisher
    form_class = PublisherForm
    action_kind = "CREATE"

    def get_success_url(self):
        return reverse("publisher_detail", args=[self.object.pk])


class TitleListView(ListView):
    model = Title

    def get_queryset(self):
        qs = super(TitleListView, self).get_queryset()
        qs = qs.order_by("name")
        return qs


class TitleDetailView(DetailView):
    model = Title


class TitleEditView(LoginRequiredMixin, EventLogMixin, UpdateView):
    model = Title
    form_class = TitleForm
    action_kind = "EDIT"

    def get_success_url(self):
        return reverse("title_detail", args=[self.object.slug])


class TitleCreateView(LoginRequiredMixin, EventLogMixin, CreateView):
    model = Title
    form_class = TitleForm
    action_kind = "CREATE"

    def get_success_url(self):
        return reverse("title_detail", args=[self.object.slug])


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
        print self.object.language.pk
        return reverse("language_detail", args=[self.object.language.pk])

    def get_context_data(self, **kwargs):
        context = super(ResourceEditView, self).get_context_data(**kwargs)
        context.update({
            "language": self.object.language,
        })
        return context