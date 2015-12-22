from django.shortcuts import render
from django.views.generic import TemplateView

from account.mixins import LoginRequiredMixin

from td.models import Region


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "gl_tracking/dashboard.html"


class PhaseProgressView(LoginRequiredMixin, TemplateView):
    template_name = "gl_tracking/phase_progress.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super(PhaseProgressView, self).get_context_data(**kwargs)
        context["phase"] = self.request.POST["phase"]
        context["regions"] = Region.objects.all()
        return context
