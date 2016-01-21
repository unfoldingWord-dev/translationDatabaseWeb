from django.shortcuts import render, redirect
# from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView, UpdateView

from account.mixins import LoginRequiredMixin

from td.models import Language, Region
from td.gl_tracking.models import Document, Progress, Phase
from td.gl_tracking.forms import VariantSplitModalForm, ProgressForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "gl_tracking/dashboard.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["phases"] = Phase.objects.all()
        return context


class PhaseView(LoginRequiredMixin, TemplateView):
    template_name = "gl_tracking/_phase_view.html"

    def post(self, request, *args, **kwargs):
        """
        Overriden to allow POST and avoid error when doing so.
        POST will be the default method of calling this view.
        """
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super(PhaseView, self).get_context_data(**kwargs)
        #
        regions = map_gls(Language.objects.filter(gateway_flag=True, variant_of=None))
        for key, region in regions.iteritems():
            region["regional_progress"] = get_regional_progress(region["gateway_languages"], self.request.POST["phase"])
        #
        context["phase"] = self.request.POST["phase"]
        context["regions"] = regions
        context["overall_progress"] = get_overall_progress(context["regions"])
        context["can_edit"] = get_edit_privilege(self.request.user.username)

        return context


class RegionDetailView(LoginRequiredMixin, DetailView):
    model = Region
    template_name = "gl_tracking/_region_detail.html"

    def post(self, request, *args, **kwargs):
        """
        Overriden to allow POST and avoid error when doing so.
        POST will be the default method of calling this view.
        """
        context = self.get_context_data()
        return self.render_to_response(context)


class VariantSplitView(LoginRequiredMixin, FormView):
    template_name = "gl_tracking/variant_split_modal_form.html"
    form_class = VariantSplitModalForm

    def get_context_data(self, *args, **kwargs):
        # Add language context based on the argument in URL
        context = super(VariantSplitView, self).get_context_data(**kwargs)
        context["language"] = Language.objects.get(code=self.kwargs["slug"])
        return context

    def form_valid(self, form):
        # If valid, remove variant from the language
        language = Language.objects.get(code=self.kwargs["slug"])
        variant = Language.objects.get(code=form.data.get("variant"))
        language.variants.remove(variant)
        # Render the same form but with extra context for the template.
        context = {
            "success": True,
            "language": language,
            "variant": variant,
        }
        return render(self.request, "gl_tracking/variant_split_modal_form.html", context)


class ProgressEditView(LoginRequiredMixin, UpdateView):
    model = Progress
    form_class = ProgressForm
    template_name_suffix = "_update_modal_form"

    def form_valid(self, form):
        self.object = form.save()
        # Render the same form but with extra context for the template.
        context = {
            "success": True,
            "object": self.object,
        }
        return render(self.request, "gl_tracking/progress_update_modal_form.html", context)


# ---------------------- #
#    CUSTOM FUNCTIONS    #
# ---------------------- #

def map_gls(gls):
    regions = {}
    for lang in gls:
        region = lang.lr
        if region:
            if region not in regions:
                regions[region] = {}
                regions[region]["gateway_languages"] = []
            regions[region]["gateway_languages"].append(lang)
        else:
            if "unknown" not in regions:
                regions["unknown"] = {}
                regions["unknown"]["gateway_languages"] = []
            regions["unknown"]["gateway_languages"].append(lang)
    return regions


def get_regional_progress(gateway_languages, phase):
    total = 0.0
    count = 0
    for lang in gateway_languages:
        count = count + 1
        if phase == "1":
            total += lang.progress_phase_1
        elif phase == "2":
            total += lang.progress_phase_2
    if count:
        return round(total / count, 2)
    else:
        return 0.0


def get_overall_progress(regions):
    total = 0.0
    count = 0
    for key, region in regions.iteritems():
        count += 1
        total += region["regional_progress"]
    if count:
        return round(total / count, 2)
    else:
        return 0.0


def get_edit_privilege(username):
    # Initialize default permission (all False)
    permission = []

    # Check if user is a gateway language coordinator
    # If he is, get the region he is responsible for
    # Append that region to the persmission list
    for region in Region.objects.all():
        permission.append(region.slug)

    print '\nGETTING PRIVILEGE FOR: ', username, permission

    return permission
