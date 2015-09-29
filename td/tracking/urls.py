from django.conf.urls import url

from .views import (
    TemplateView,
    AjaxCharterListView,
    # CharterListView,
    charter,
    CharterAdd,
    CharterUpdate,
    SuccessView,
    # event,
    EventAddView,
    charters_autocomplete,
)

urlpatterns = [

    url(r"^$", TemplateView.as_view(template_name="tracking/project_list.html"), name="project_list"),
    url(r"ajax/charters/$", AjaxCharterListView.as_view(), name="ajax_ds_charter_list"),

    url(r"^charter/new/$", CharterAdd.as_view(), name="charter_add"),
    url(r"^charter/update/(?P<pk>\d+)/$", CharterUpdate.as_view(), name="charter_update"),
    url(r"^success/(?P<obj_type>[A-Za-z]+)/(?P<pk>\d+)/$", SuccessView.as_view(), name="charter_add_success"),
    # url(r"^charter/new/success/(?P<pk>\d+)/$", charter_add_success, name="charter_add_success"),

    url(r"^ac/charters$", charters_autocomplete, name="charters_autocomplete"),

    url(r"^charter/detail/(?P<pk>\d+)/$", charter, name="charter"),

    # Under Construction
    url(r'^event/detail/(?P<event_id>\d+)/$', TemplateView.as_view(template_name='tracking/under_construction.html'), name='event'),
    url(r'^event/new/(?P<pk>\d+)/$', TemplateView.as_view(template_name='tracking/under_construction.html'), name='event_add_specific'),
    url(r'^event/new/$', EventAddView.as_view(), name='event_add'),
    # url(r'^event/add/success/$', views.event_add_success, name = 'event_add_success'),
    # url(r'^event/add/fail/$', views.event_add_fail, name = 'event_add_fail'),
]
