from django.conf.urls import patterns, url

from .views import (
    CountryListView,
    CountryDetailView,
    CountryEditView,
    LanguageCreateView,
    LanguageDetailView,
    LanguageEditView,
    NetworkCreateView,
    NetworkDetailView,
    NetworkEditView,
    NetworkListView,
    WIPCreateView,
    ScriptureCreateView,
    TranslationNeedCreateView,
    ResourceCreateView,
    WIPEditView,
    ScriptureEditView,
    TranslationNeedEditView,
    ResourceEditView,
)


urlpatterns = patterns(
    "",
    url(r"networks/$", NetworkListView.as_view(), name="network_list"),
    url(r"networks/create/$", NetworkCreateView.as_view(), name="network_create"),
    url(r"networks/(?P<pk>\d+)/$", NetworkDetailView.as_view(), name="network_detail"),
    url(r"networks/(?P<pk>\d+)/edit/$", NetworkEditView.as_view(), name="network_edit"),

    url(r"countries/$", CountryListView.as_view(), name="country_list"),
    url(r"countries/(?P<pk>\d+)/$", CountryDetailView.as_view(), name="country_detail"),
    url(r"countries/(?P<pk>\d+)/edit/$", CountryEditView.as_view(), name="country_edit"),
    url(r"countries/(?P<pk>\d+)/languages/create/$", LanguageCreateView.as_view(), name="language_create"),

    url(r"languages/(?P<pk>\d+)/$", LanguageDetailView.as_view(), name="language_detail"),
    url(r"languages/(?P<pk>\d+)/edit/$", LanguageEditView.as_view(), name="language_edit"),
    url(r"languages/(?P<pk>\d+)/works-in-progress/create/$", WIPCreateView.as_view(), name="wip_create"),
    url(r"languages/(?P<pk>\d+)/scriptures/create/$", ScriptureCreateView.as_view(), name="scripture_create"),
    url(r"languages/(?P<pk>\d+)/translation-needs/create/$", TranslationNeedCreateView.as_view(), name="translation_need_create"),
    url(r"languages/(?P<pk>\d+)/resources/create/$", ResourceCreateView.as_view(), name="resource_create"),

    url(r"works-in-progress/(?P<pk>\d+)/edit/$", WIPEditView.as_view(), name="wip_edit"),
    url(r"scriptures/(?P<pk>\d+)/edit/$", ScriptureEditView.as_view(), name="scripture_edit"),
    url(r"translation-needs/(?P<pk>\d+)/edit/$", TranslationNeedEditView.as_view(), name="translation_need_edit"),
    url(r"resources/(?P<pk>\d+)/edit/$", ResourceEditView.as_view(), name="resource_edit"),
)
