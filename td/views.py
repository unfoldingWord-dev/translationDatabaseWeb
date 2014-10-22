from django.http import HttpResponse
from django.views.generic import ListView

from td.imports.models import (
    EthnologueCountryCode,
    EthnologueLanguageCode,
    EthnologueLanguageIndex,
    SIL_ISO_639_3,
    WikipediaISOLanguage
)

from .exports import LanguageCodesExport, LanguageNamesExport
from .models import AdditionalLanguage


def codes_text_export(request):
    return HttpResponse(LanguageCodesExport().text, content_type="text/plain")


def names_text_export(reqeust):
    return HttpResponse(LanguageNamesExport().text, content_type="text/plain")


def names_json_export(request):
    return HttpResponse(LanguageNamesExport().json, content_type="application/json")


class AdditionalLanguageListView(ListView):
    model = AdditionalLanguage
    paginate_by = 50


class EthnologueCountryCodeListView(ListView):
    model = EthnologueCountryCode
    template_name = "td/ethnologuecountrycode_list.html"
    paginate_by = 50


class EthnologueLanguageCodeListView(ListView):
    model = EthnologueLanguageCode
    template_name = "td/ethnologuelanguagecode_list.html"
    paginate_by = 50


class EthnologueLanguageIndexListView(ListView):
    model = EthnologueLanguageIndex
    template_name = "td/ethnologuelanguageindex_list.html"
    paginate_by = 50


class SIL_ISO_639_3ListView(ListView):
    model = SIL_ISO_639_3
    template_name = "td/sil_list.html"
    paginate_by = 50


class WikipediaISOLanguageListView(ListView):
    model = WikipediaISOLanguage
    template_name = "td/wikipedia_list.html"
