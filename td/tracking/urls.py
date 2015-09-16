from django.conf.urls import url

from .views import (
    AjaxCharterListView,
    CharterListView,
    # charter,
    CharterAdd,
    CharterUpdate,
    charter_add_success,
    # event,
    # EventAddView,
    charters_autocomplete,
    UnderConstructionView,
)

urlpatterns = [

    url(r'^$', CharterListView.as_view(), name='project_list'),
    url(r'ajax/charters/$', AjaxCharterListView.as_view(), name='ajax_ds_charter_list'),

    url(r'^charter/detail/(?P<pk>\d+)/$', UnderConstructionView.as_view(), name='charter'),
    url(r'^charter/new/$', CharterAdd.as_view(), name='charter_add'),
    url(r'^charter/update/(?P<pk>\d+)/$', CharterUpdate.as_view(), name='charter_update'),
    url(r'^charter/new/success/(?P<pk>\d+)/$', charter_add_success, name='charter_add_success'),

    url(r'^ac/charters$', charters_autocomplete, name="charters_autocomplete"),

    url(r'^event/detail/(?P<event_id>\d+)/$', UnderConstructionView.as_view(), name='event'),
    url(r'^event/new/$', UnderConstructionView.as_view(), name='event_add'),
    # url(r'^event/new/$', EventAddView.as_view(), name='event_add'),
    url(r'^event/new/(?P<pk>\d+)/$', UnderConstructionView.as_view(), name='event_add_specific'),
    # url(r'^event/add/success/$', views.event_add_success, name = 'event_add_success'),
    # url(r'^event/add/fail/$', views.event_add_fail, name = 'event_add_fail'),

]
