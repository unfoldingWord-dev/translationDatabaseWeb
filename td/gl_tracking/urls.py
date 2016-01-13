from django.conf.urls import url

from td.gl_tracking.views import HomeView, PhaseProgressView, RegionDetailView, VariantSplitView

urlpatterns = [

    # Home
    url(r"^$", HomeView.as_view(), name="home"),

    # Phases
    url(r"^ajax/phase_progress/$", PhaseProgressView.as_view(), name="ajax_phase_progress"),
    url(r"^ajax/region_detail/(?P<slug>[a-z]+)/$", RegionDetailView.as_view(), name="ajax_region_detail"),
    url(r"^ajax/variant_split_modal/(?P<slug>[a-z]+)/$", VariantSplitView.as_view(), name="ajax_modal_variant_split"),

]
