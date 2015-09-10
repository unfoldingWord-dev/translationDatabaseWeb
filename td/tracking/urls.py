from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (
    AjaxCharterListView,
    CharterListView,
    charter,
    CharterAdd,
    CharterUpdate,
    charter_add_success,
    # event,
    EventAdd,
    UnderConstructionView,
)

urlpatterns = [

    url(r'^$', CharterListView.as_view(), name='project_list'),
    url(r'ajax/charters/$', AjaxCharterListView.as_view(), name='ajax_ds_charter_list'),

    url(r'^charter/detail/(?P<pk>\d+)/$', charter, name='charter'),
    url(r'^charter/new/$', CharterAdd.as_view(), name='charter_add'),
    url(r'^charter/update/(?P<pk>\d+)/$', CharterUpdate.as_view(), name='charter_update'),
    url(r'^charter/new/success/(?P<pk>\d+)/$', charter_add_success, name='charter_add_success'),

    # url(r'^event/detail/(?P<event_id>[0-9a-zA-Z])+/$', event, name='event'),
    url(r'^event/new/$', UnderConstructionView.as_view(), name='event_add'),
    url(r'^event/new/(?P<pk>\d+)/$', UnderConstructionView.as_view(), name='event_add_specific'),
    # url(r'^event/add/success/$', views.event_add_success, name = 'event_add_success'),
    # url(r'^event/add/fail/$', views.event_add_fail, name = 'event_add_fail'),

]
