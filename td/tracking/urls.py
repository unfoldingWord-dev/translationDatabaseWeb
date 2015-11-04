from django.conf.urls import url

from .views import (
    AjaxCharterListView,
    AjaxCharterEventsListView,
    charters_autocomplete,
    charters_autocomplete_lid,
    CharterAdd,
    CharterUpdate,
    EventAddView,
    EventUpdateView,
    EventDetailView,
    SuccessView,
    MultiCharterEventView,
    MultiCharterSuccessView,
    NewCharterModalView,
    NewItemView,
    HomeView,
)

urlpatterns = [

    # Home
    url(r"^$", HomeView.as_view(), name="project_list"),

    # Charter
    url(r"^charter/new/$", CharterAdd.as_view(), name="charter_add"),
    url(r"^charter/update/(?P<pk>\d+)/$", CharterUpdate.as_view(), name="charter_update"),

    # Event
    url(r"^event/new/$", EventAddView.as_view(), name="event_add"),
    url(r"^event/new/(?P<pk>\d+)/$", EventAddView.as_view(), name="event_add_specific"),
    url(r"^event/update/(?P<pk>\d+)/$", EventUpdateView.as_view(), name="event_update"),
    url(r"^event/detail/(?P<pk>\d+)/$", EventDetailView.as_view(), name="event_detail"),

    url(r"^mc-event/new/$", MultiCharterEventView.as_view(), name="multi_charter_event_add"),

    # Others
    url(r"^ajax/charter_events/(?P<pk>\d+)/$", AjaxCharterEventsListView.as_view(), name="ajax_charter_events"),
    url(r"^ajax/charters/$", AjaxCharterListView.as_view(), name="ajax_ds_charter_list"),
    url(r"^ac/charters$", charters_autocomplete, name="charters_autocomplete"),
    url(r"^ac/charters/lid$", charters_autocomplete_lid, name="charters_autocomplete_lid"),
    url(r"^success/(?P<obj_type>[A-Za-z]+)/(?P<pk>\d+)/$", SuccessView.as_view(), name="charter_add_success"),
    url(r"^success/mc-event/$", MultiCharterSuccessView.as_view(), name="multi_charter_success"),
    url(r"^new_item/$", NewItemView.as_view(), name="new_item"),

    # Under Construction
    url(r"^ajax/charter/modal/$", NewCharterModalView.as_view(), name="new_charter_modal"),
]
