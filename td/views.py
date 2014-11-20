from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from td.imports.models import (
    EthnologueCountryCode,
    EthnologueLanguageCode,
    EthnologueLanguageIndex,
    SIL_ISO_639_3,
    WikipediaISOLanguage
)

from .models import AdditionalLanguage, Language
from .utils import DataTableSourceView


def codes_text_export(request):
    return HttpResponse(Language.codes_text(), content_type="text/plain")


def names_text_export(reqeust):
    return HttpResponse(Language.names_text(), content_type="text/plain")


def names_json_export(request):
    return JsonResponse(Language.names_data(), safe=False)  # Set safe to False to allow list instead of dict to be returned


class AdditionalLanguageListView(TemplateView):
    template_name = "td/additionallanguage_list.html"


class EthnologueCountryCodeListView(TemplateView):
    template_name = "td/ethnologuecountrycode_list.html"


class EthnologueLanguageCodeListView(TemplateView):
    template_name = "td/ethnologuelanguagecode_list.html"


class EthnologueLanguageIndexListView(TemplateView):
    template_name = "td/ethnologuelanguageindex_list.html"


class SIL_ISO_639_3ListView(TemplateView):
    template_name = "td/sil_list.html"


class WikipediaISOLanguageListView(TemplateView):
    template_name = "td/wikipedia_list.html"


class AjaxAdditionalLanguageListView(DataTableSourceView):
    model = AdditionalLanguage
    fields = [
        "ietf_tag",
        "two_letter",
        "three_letter",
        "common_name",
        "native_name",
        "comment"
    ]


class AjaxEthnologueCountryCodeListView(DataTableSourceView):
    model = EthnologueCountryCode
    fields = [
        "code",
        "name",
        "area"
    ]


class AjaxEthnologueLanguageCodeListView(DataTableSourceView):
    model = EthnologueLanguageCode
    fields = [
        "code",
        "country_code",
        "status",
        "name"
    ]


class AjaxEthnologueLanguageIndexListView(DataTableSourceView):
    model = EthnologueLanguageIndex
    fields = [
        "language_code",
        "country_code",
        "name_type",
        "name"
    ]


class AjaxSIL_ISO_639_3ListView(DataTableSourceView):
    model = SIL_ISO_639_3
    fields = [
        "code",
        "part_2b",
        "part_2t",
        "part_1",
        "scope",
        "language_type",
        "ref_name",
        "comment"
    ]


class AjaxWikipediaISOLanguageListView(DataTableSourceView):
    model = WikipediaISOLanguage
    fields = [
        "language_family",
        "language_name",
        "native_name",
        "iso_639_1",
        "iso_639_2t",
        "iso_639_2b",
        "iso_639_3",
        "iso_639_9",
        "notes"
    ]
