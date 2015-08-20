from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	
	# url(r'^charter/?P<proj_num>[0-9a-zA-Z]+/$', views.charter, name = 'charter'),
	# url(r'^charter/add/$', views.charter_add, name = 'charter_add'),
	# url(r'^charter/add/success/$', views.charter_added, name = 'charter_added'),
	# url(r'^charter/add/fail/$', views.charter_added, name = 'charter_added'),

	# url(r'^event/?P<proj_num>[0-9a-zA-Z]+/$', views.event, name = 'event'),
	# url(r'^event/add/$', views.event_add, name = 'event_add'),
	# url(r'^event/add/success/$', views.event_added, name = 'event_added'),
	# url(r'^event/add/fail/$', views.event_added, name = 'event_added'),

]