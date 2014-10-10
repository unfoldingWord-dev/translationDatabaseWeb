from django.http import HttpResponse

from .exports import LanguageCodesExport, LanguageNamesExport


def codes_text_export(request):
    return HttpResponse(LanguageCodesExport().text, content_type="text/plain")


def names_text_export(reqeust):
    return HttpResponse(LanguageNamesExport().text, content_type="text/plain")


def names_json_export(request):
    return HttpResponse(LanguageNamesExport().json, content_type="application/json")
