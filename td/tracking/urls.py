from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (
	index,
	charter,
	charter_add,
	charter_add_success,
	event,
	event_add,
)

urlpatterns = [
	url(r'^$', index, name = 'index'),
	
	url(r'^charter/detail/(?P<target_lang_name>[0-9a-zA-Z]+)/$', charter, name = 'charter'),
	url(r'^charter/add/$', charter_add.as_view(), name = 'charter_add'),
	url(r'^charter/add/success/$', charter_add_success, name = 'charter_add_success'),
	# url(r'^charter/add/fail/$', views.charter_add_fail, name = 'charter_add_fail'),

	url(r'^event/detail/(?P<event_id>[0-9a-zA-Z])+/$', event, name = 'event'),
	url(r'^event/add/$', event_add, name = 'event_add'),
	# url(r'^event/add/success/$', views.event_add_success, name = 'event_add_success'),
	# url(r'^event/add/fail/$', views.event_add_fail, name = 'event_add_fail'),

]