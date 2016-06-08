from django.conf.urls import url

from td.gl_tracking.views import(
    HomeView, PhaseView, RegionDetailView, VariantSplitView,
    ProgressEditView, PartnerListView, PartnerDetailView,
    PartnerEditView, PartnerCreateView, AjaxPartnerListView,
    RegionAssignmentView
)

urlpatterns = [

    # Home
    url(r"^$", HomeView.as_view(), name="home"),

    # Phases
    url(r"^ajax/phase_progress/(?P<phase>\d+)/$", PhaseView.as_view(), name="ajax_phase_view"),
    url(r"^ajax/region_detail/(?P<slug>[a-z]+)/$", RegionDetailView.as_view(), name="ajax_region_detail"),
    url(r"^ajax/variant_split_modal/(?P<slug>[0-9a-z\-]+)/$", VariantSplitView.as_view(), name="ajax_modal_variant_split"),

    url(r"^progress/change/(?P<pk>[\d+]+)/$", ProgressEditView.as_view(), name="change_progress"),
    url(r"^region_assignment/$", RegionAssignmentView.as_view(), name="region_assignment"),
    url(r"^partners/$", PartnerListView.as_view(), name="partner_list_view"),
    url(r"^partners/(?P<pk>[0-9]+)$", PartnerDetailView.as_view(), name="partner_detail_view"),
    url(r"^partners/(?P<pk>[0-9]+)/edit$", PartnerEditView.as_view(), name="partner_edit_view"),
    url(r"^partners/new$", PartnerCreateView.as_view(), name="partner_create_view"),
    url(r"^ajax/partners/$", AjaxPartnerListView.as_view(), name="ajax_partner_list"),

]
