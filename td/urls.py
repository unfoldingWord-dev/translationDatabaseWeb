from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from .views import (
    AdditionalLanguageListView,
    EthnologueCountryCodeListView,
    EthnologueLanguageCodeListView,
    EthnologueLanguageIndexListView,
    SIL_ISO_639_3ListView,
    WikipediaISOLanguageListView,
    IMBPeopleGroupListView,
    AjaxAdditionalLanguageListView,
    AjaxEthnologueCountryCodeListView,
    AjaxEthnologueLanguageCodeListView,
    AjaxEthnologueLanguageIndexListView,
    AjaxSIL_ISO_639_3ListView,
    AjaxWikipediaISOLanguageListView,
    AjaxIMBPeopleGroupListView,
    codes_text_export,
    names_text_export,
    names_json_export,
    export_svg,
    languages_autocomplete,
)

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^siteadmin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^invites/", include("pinax.invitations.urls")),

    url(r"^exports/codes-d43.txt$", codes_text_export, name="codes_text_export"),
    url(r"^exports/langnames.txt$", names_text_export, name="names_text_export"),
    url(r"^exports/langnames.json$", names_json_export, name="names_json_export"),
    url(r"^exports/gatewaylanguages-map/$", export_svg, name="gateway_languages_map_export"),

    url(r"^uw/", include("td.resources.urls")),
    url(r"^uw/", include("td.urls_languages")),

    url(r"^publishing/", include("td.publishing.urls")),
    url(r"^api/", include("td.urls_api")),
    url(r"^tracking/", include("td.tracking.urls", namespace="tracking")),
    url(r"^gl/", include("td.gl_tracking.urls", namespace="gl")),
    url(r"^api/", include("td.api.urls", namespace="api")),
    url(r"^comment/", include("td.commenting.urls", namespace="comment")),
    url(r"^comments/", include("django_comments.urls")),

    url(r"^data-sources/additional-languages/$", AdditionalLanguageListView.as_view(), name="ds_additional_languages"),
    url(r"^data-sources/ethnologue/country-codes/$", EthnologueCountryCodeListView.as_view(), name="ds_ethnologue_country_codes"),
    url(r"^data-sources/ethnologue/language-codes/$", EthnologueLanguageCodeListView.as_view(), name="ds_ethnologue_language_codes"),
    url(r"^data-sources/ethnologue/language-index/$", EthnologueLanguageIndexListView.as_view(), name="ds_ethnologue_language_index"),
    url(r"^data-sources/sil-iso-639-3/$", SIL_ISO_639_3ListView.as_view(), name="ds_sil"),
    url(r"^data-sources/wikipedia/$", WikipediaISOLanguageListView.as_view(), name="ds_wikipedia"),
    url(r"^data-sources/imb/peoplegroups/$", IMBPeopleGroupListView.as_view(), name="ds_imb_peoplegroups"),

    url(r"^ajax/data-sources/additional-languages/$", AjaxAdditionalLanguageListView.as_view(), name="ajax_ds_additional_languages"),
    url(r"^ajax/data-sources/ethnologue/country-codes/$", AjaxEthnologueCountryCodeListView.as_view(), name="ajax_ds_ethnologue_country_codes"),
    url(r"^ajax/data-sources/ethnologue/language-codes/$", AjaxEthnologueLanguageCodeListView.as_view(), name="ajax_ds_ethnologue_language_codes"),
    url(r"^ajax/data-sources/ethnologue/language-index/$", AjaxEthnologueLanguageIndexListView.as_view(), name="ajax_ds_ethnologue_language_index"),
    url(r"^ajax/data-sources/sil-iso-639-3/$", AjaxSIL_ISO_639_3ListView.as_view(), name="ajax_ds_sil"),
    url(r"^ajax/data-sources/wikipedia/$", AjaxWikipediaISOLanguageListView.as_view(), name="ajax_ds_wikipedia"),
    url(r"^ajax/data-sources/imb/peoplegroups/$", AjaxIMBPeopleGroupListView.as_view(), name="ajax_ds_imb_peoplegroups"),

    url(r"^ac/langnames/", languages_autocomplete, name="names_autocomplete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
