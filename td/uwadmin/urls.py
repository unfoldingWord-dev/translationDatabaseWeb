from django.conf.urls import patterns, url
from django.views.generic import TemplateView


from .views import (
    ajax_language_version,
    api_contact,
    ContactList,
    ContactCreate,
    ContactDetail,
    ContactUpdate,
    languages_autocomplete,
    OpenBibleStoryListView,
    OpenBibleStoryCreateView,
    OpenBibleStoryDetailView,
    OpenBibleStoryUpdateView,
    PublishRequestCreateView,
    PublishRequestUpdateView,
    PublishRequestDeleteView,
    source_languages_autocomplete,
)


urlpatterns = patterns(
    "",
    url(r"^$", TemplateView.as_view(template_name="uwadmin/homepage.html"), name="home"),
    url(r"^api/contacts/", api_contact, name="api_contacts"),
    url(r"^contacts/$", ContactList.as_view(), name="contact_list"),
    url(r"^contacts/create/$", ContactCreate.as_view(), name="contact_create"),
    url(r"^contacts/(?P<pk>\d+)/$", ContactDetail.as_view(), name="contact_detail"),
    url(r"^contacts/(?P<pk>\d+)/update/$", ContactUpdate.as_view(), name="contact_update"),
    url(r"^obs/$", OpenBibleStoryListView.as_view(), name="obs_list"),
    url(r"^obs/create/$", OpenBibleStoryCreateView.as_view(), name="obs_create"),
    url(r"^obs/(?P<pk>\d+)/$", OpenBibleStoryDetailView.as_view(), name="obs_detail"),
    url(r"^obs/(?P<code>[\w-]+)/update/$", OpenBibleStoryUpdateView.as_view(), name="obs_update"),
    url(r"^publish/request/$", PublishRequestCreateView.as_view(), name="publish_request"),
    url(r"^publish/request/(?P<pk>\d+)", PublishRequestUpdateView.as_view(), name="publish_request_update"),
    url(r"^publish/request-reject/(?P<pk>\d+)", PublishRequestDeleteView.as_view(), name="publish_request_delete"),
    url(r"^ac/langnames/", languages_autocomplete, name="names_autocomplete"),
    url(r"^ac/src-langnames/", source_languages_autocomplete, name="source_names_autocomplete"),
    url(r"^ajax/langversion/", ajax_language_version, name="ajax_language_version")
)
