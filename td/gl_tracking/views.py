from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, CreateView
from django.views.generic.edit import FormView, UpdateView
from django.core.urlresolvers import reverse_lazy

from account.mixins import LoginRequiredMixin

from td.models import Language, WARegion
from td.utils import DataTableSourceView
from td.gl_tracking.models import Progress, Phase, GLDirector, Partner
from td.gl_tracking.forms import VariantSplitModalForm, ProgressForm, RegionAssignmentModalForm, PartnerForm


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
        context["can_edit"] = get_edit_privilege(self.request.user)

        return context


class RegionDetailView(LoginRequiredMixin, DetailView):
    model = WARegion
    template_name = "gl_tracking/_region_detail.html"

    def post(self, request, *args, **kwargs):
        """
        Overriden to allow POST and avoid error when doing so.
        POST will be the default method of calling this view.
        """
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super(RegionDetailView, self).get_context_data(**kwargs)
        context["directors"] = self.object.gldirector_set.all()
        return context


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


class RegionAssignmentView(LoginRequiredMixin, FormView):

    template_name = "gl_tracking/region_assignment_modal_form.html"
    form_class = RegionAssignmentModalForm

    def get_context_data(self, *args, **kwargs):
        context = super(RegionAssignmentView, self).get_context_data(**kwargs)
        context["wa_regions"] = WARegion.objects.all()
        context["gl_directors"] = GLDirector.objects.filter(is_helper=False)
        context["gl_helpers"] = GLDirector.objects.filter(is_helper=True)
        return context

    def form_valid(self, form):
        # Clear any existing assignments
        for director in GLDirector.objects.all():
            director.regions.clear()
        # Go through the form data and assign GLDirector to regions
        for key in form.data:
            region = key.split("_")[0]
            if region in WARegion.slug_all():
                region_obj = WARegion.objects.get(slug=region)
                for user in form.data.getlist(key):
                    gldirector = GLDirector.objects.get(user__username=user)
                    gldirector.regions.add(region_obj)
        # Render the same form but with extra context for the template.
        context = {
            "success": True
        }
        return render(self.request, "gl_tracking/region_assignment_modal_form.html", context)


class PartnerListView(LoginRequiredMixin, TemplateView):
    template_name = "gl_tracking/partner_list.html"


class PartnerDetailView(LoginRequiredMixin, DetailView):
    model = Partner
    context_object_name = "partner"


class PartnerEditView(LoginRequiredMixin, UpdateView):
    model = Partner
    form_class = PartnerForm


class PartnerCreateView(LoginRequiredMixin, CreateView):
    model = Partner
    form_class = PartnerForm
    success_url = reverse_lazy("gl:partner_list_view")


class AjaxPartnerListView(LoginRequiredMixin, DataTableSourceView):
    model = Partner

    fields = ["name", "country__name", "is_active"]
    link_column = "name"
    link_url_name = "gl:partner_detail_view"
    link_url_field = "pk"


# ---------------------- #
#    CUSTOM FUNCTIONS    #
# ---------------------- #

def map_gls(gls):
    regions = {}
    for lang in gls:
        region = lang.wa_region
        if region:
            if region.slug not in regions:
                regions[region.slug] = {"name": region.name}
                regions[region.slug]["gateway_languages"] = []
            regions[region.slug]["gateway_languages"].append(lang)
        else:
            if "unknown" not in regions:
                regions["unknown"] = {"name": "Unknown"}
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


def get_edit_privilege(user):
    permission = []

    if hasattr(user, "gldirector"):
        for region in user.gldirector.regions.all():
            permission.append(region.slug)

    return permission
