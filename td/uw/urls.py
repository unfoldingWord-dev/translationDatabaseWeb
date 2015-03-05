from django.conf.urls import patterns, url

from .views import (
    HomeView,
    RegionListView,
    RegionDetailView,
    CountryListView,
    CountryDetailView,
    CountryEditView,
    LanguageCreateView,
    LanguageDetailView,
    LanguageEditView,
    LanguageListView,
    AjaxLanguageListView,
    NetworkCreateView,
    NetworkDetailView,
    NetworkEditView,
    NetworkListView,
    ResourceCreateView,
    ResourceEditView,
    country_tree_data,
    upload_gateway_flag_file,
)


urlpatterns = patterns(
    "",
    url(r"^$", HomeView.as_view(), name="uw_home"),
    url(r"networks/$", NetworkListView.as_view(), name="network_list"),
    url(r"networks/create/$", NetworkCreateView.as_view(), name="network_create"),
    url(r"networks/(?P<pk>\d+)/$", NetworkDetailView.as_view(), name="network_detail"),
    url(r"networks/(?P<pk>\d+)/edit/$", NetworkEditView.as_view(), name="network_edit"),

    url(r"regions/$", RegionListView.as_view(), name="region_list"),
    url(r"regions/(?P<slug>\w+)/$", RegionDetailView.as_view(), name="region_detail"),
    url(r"countries/$", CountryListView.as_view(), name="country_list"),
    url(r"countries/(?P<pk>\d+)/$", CountryDetailView.as_view(), name="country_detail"),
    url(r"countries/(?P<pk>\d+)/edit/$", CountryEditView.as_view(), name="country_edit"),
    url(r"countries/(?P<pk>\d+)/languages/create/$", LanguageCreateView.as_view(), name="language_create"),
    url(r"ajax/languages/$", AjaxLanguageListView.as_view(), name="ajax_ds_uw_languages"),
    url(r"languages/$", LanguageListView.as_view(), name="language_list"),
    url(r"languages/(?P<pk>\d+)/$", LanguageDetailView.as_view(), name="language_detail"),
    url(r"languages/(?P<pk>\d+)/edit/$", LanguageEditView.as_view(), name="language_edit"),
    url(r"languages/(?P<pk>\d+)/resources/create/$", ResourceCreateView.as_view(), name="resource_create"),

    url(r"gateway_language_flag/upload/$", upload_gateway_flag_file, name="gateway_flag_upload"),

    url(r"resources/(?P<pk>\d+)/edit/$", ResourceEditView.as_view(), name="resource_edit"),

    url(r"country_gateways.json$", country_tree_data, name="country_tree_data")
)
