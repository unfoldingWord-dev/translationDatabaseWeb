from django.conf.urls import url

from td.gl_tracking.views import HomeView, PhaseProgressView

urlpatterns = [

    # Home
    url(r"^$", HomeView.as_view(), name="home"),

    # Phases
    url(r"^phase_progress/$", PhaseProgressView.as_view(), name="phase_progress"),

]
