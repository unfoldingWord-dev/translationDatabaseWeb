from django.conf.urls import url

from .views import (
    AjaxCharterListView,
    AjaxCharterEventsListView,
    charters_autocomplete,
    charters_autocomplete_lid,
    CharterAddView,
    CharterUpdateView,
    downloadPDF,
    EventAddView,
    EventUpdateView,
    EventDetailView,
    FileDownloadView,
    SuccessView,
    MultiCharterEventView,
    MultiCharterSuccessView,
    NewCharterModalView,
    NewItemView,
    MultiCharterAddView,
    HomeView,
    AjaxCharterPartnerLookup,
)
urlpatterns = [

    # Home
    url(r"^$", HomeView.as_view(), name="project_list"),

    # Charter
    url(r"^charter/new/$", CharterAddView.as_view(), name="charter_add"),
    url(r"^charter/new/(?P<pk>\d+)/$", CharterAddView.as_view(), name="charter_add_specific"),
    url(r"^charter/update/(?P<pk>\d+)/$", CharterUpdateView.as_view(), name="charter_update"),
    url(r"^mc/new/$", MultiCharterAddView.as_view(), name="multi_charter_add"),

    # Event
    url(r"^event/new/$", EventAddView.as_view(), name="event_add"),
    url(r"^event/new/(?P<pk>\d+)/$", EventAddView.as_view(), name="event_add_specific"),
    url(r"^event/update/(?P<pk>\d+)/$", EventUpdateView.as_view(), name="event_update"),
    url(r"^event/detail/(?P<pk>\d+)/$", EventDetailView.as_view(), name="event_detail"),
    url(r"^mc-event/new/$", MultiCharterEventView.as_view(), name="multi_charter_event_add"),

    # Ajax
    url(r"^ajax/charter_events/(?P<pk>\d+)/$", AjaxCharterEventsListView.as_view(), name="ajax_charter_events"),
    url(r"^ajax/charters/$", AjaxCharterListView.as_view(), name="ajax_ds_charter_list"),
    url(r"^ajax/charters/(?P<slug>\w+)/$", AjaxCharterListView.as_view(), name="ajax_wa_region_charter_list"),
    url(r"^ajax/charter/modal/$", NewCharterModalView.as_view(), name="new_charter_modal"),
    url(r"^ajax/charter/partner_lookup/$", AjaxCharterPartnerLookup.as_view(), name="charter_partner_lookup"),

    # Auto-complete
    url(r"^ac/charters$", charters_autocomplete, name="charters_autocomplete"),
    url(r"^ac/charters/lid$", charters_autocomplete_lid, name="charters_autocomplete_lid"),

    # Success
    url(r"^success/(?P<obj_type>[A-Za-z]+)/(?P<pk>\d+)/$", SuccessView.as_view(), name="charter_add_success"),
    url(r"^success/mc-event/$", MultiCharterSuccessView.as_view(), name="multi_charter_success"),

    # Others
    url(r"^new_item/$", NewItemView.as_view(), name="new_item"),
    url(r"^downloads/$", FileDownloadView.as_view(), name="file_download"),
    url(r"^downloads/(?P<file_name>[A-Za-z_.]+)/$", downloadPDF, name="download_file"),

]
