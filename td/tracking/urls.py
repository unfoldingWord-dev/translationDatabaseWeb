from django.conf.urls import url

from .views import (
    AjaxCharterListView,
    AjaxCharterEventsListView,
    charter,
    charters_autocomplete,
    CharterAdd,
    CharterUpdate,
    EventAddView,
    SuccessView,
    TemplateView,
)

urlpatterns = [

    # Home
    url(r"^$", TemplateView.as_view(template_name="tracking/project_list.html"), name="project_list"),

    # Charter
    url(r"^charter/new/$", CharterAdd.as_view(), name="charter_add"),
    url(r"^charter/update/(?P<pk>\d+)/$", CharterUpdate.as_view(), name="charter_update"),
    url(r"^charter/detail/(?P<pk>\d+)/$", charter, name="charter"),

    # Event
    url(r"^event/new/$", EventAddView.as_view(), name="event_add"),
    url(r"^event/new/(?P<pk>\d+)/$", EventAddView.as_view(), name="event_add_specific"),

    # Others
    url(r"^ajax/charter_events/(?P<pk>\d+)/$", AjaxCharterEventsListView.as_view(), name="ajax_charter_events"),
    url(r"^ajax/charters/$", AjaxCharterListView.as_view(), name="ajax_ds_charter_list"),
    url(r"^ac/charters$", charters_autocomplete, name="charters_autocomplete"),
    url(r"^success/(?P<obj_type>[A-Za-z]+)/(?P<pk>\d+)/$", SuccessView.as_view(), name="charter_add_success"),

    # Under Construction
    url(r"^event/detail/(?P<pk>\d+)/$", TemplateView.as_view(template_name="tracking/under_construction.html"), name="event"),
]
