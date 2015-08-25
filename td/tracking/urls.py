from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	
	url(r'^charter/detail/(?P<target_lang_name>[0-9a-zA-Z]+)/$', views.charter, name = 'charter'),
	url(r'^charter/add/$', views.charter_add, name = 'charter_add'),
	url(r'^charter/add/success/$', views.charter_add_success, name = 'charter_add_success'),
	# url(r'^charter/add/fail/$', views.charter_add_fail, name = 'charter_add_fail'),

	url(r'^event/detail/(?P<event_id>[0-9a-zA-Z])+/$', views.event, name = 'event'),
	url(r'^event/add/$', views.event_add, name = 'event_add'),
	# url(r'^event/add/success/$', views.event_add_success, name = 'event_add_success'),
	# url(r'^event/add/fail/$', views.event_add_fail, name = 'event_add_fail'),

]