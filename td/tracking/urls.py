from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^add_charter/$', views.add_charter, name = 'add_charter'),
	url(r'^add_event/$', views.add_event, name = 'add_event'),
	url(r'^add_charter/success/$', views.charter_added, name = 'charter_added'),
	url(r'^add_event/success$', views.event_added, name = 'event_added'),
]