from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from td.imports.models import (
    EthnologueCountryCode,
    EthnologueLanguageCode,
    EthnologueLanguageIndex,
    SIL_ISO_639_3,
    WikipediaISOLanguage,
    IMBPeopleGroup
)

from td.uw.models import Language
from .models import AdditionalLanguage

from .utils import DataTableSourceView, svg_to_pdf


def codes_text_export(request):
    return HttpResponse(Language.codes_text(), content_type="text/plain")


def names_text_export(request):
    return HttpResponse(Language.names_text(), content_type="text/plain")


def names_json_export(request):
    data = cache_get_or_set("langnames", Language.names_data)
    return JsonResponse(data, safe=False)  # Set safe to False to allow list instead of dict to be returned


def cache_get_or_set(key, acallable):
    data = cache.get(key)
    if data is None:
        data = acallable()
        cache.set(key, data, None)
    return data


@csrf_exempt
def export_svg(request):
    svg = request.POST.get("data")
    response = HttpResponse(content_type="application/pdf")
    response.write(svg_to_pdf(svg))
    response["Content-Disposition"] = "attachment; filename=gateway_languages_map.pdf"
    return response


def languages_autocomplete(request):
    term = request.GET.get("q").lower()
    data = cache_get_or_set("langnames", Language.names_data)
    d = []
    if len(term) <= 3:
        term = term.encode("utf-8")
        # search: cc, lc
        # first do a *starts with* style search of language code (lc)
        d.extend([
            x
            for x in data
            if term == x["lc"].lower()[:len(term)]
        ])
        d.extend([
            x
            for x in data
            if term in [y.lower() for y in x["cc"]]
        ])
    if len(term) >= 3:
        # search: lc, ln, lr
        term = term.encode("utf-8")
        d.extend([
            x
            for x in data
            if term in x["lc"] or term in x["ln"].lower() or term in x["lr"].lower()
        ])
    return JsonResponse({"results": d, "count": len(d), "term": term})


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


class IMBPeopleGroupListView(TemplateView):
    template_name = "td/imbpeoplegroup_list.html"


class AjaxAdditionalLanguageListView(DataTableSourceView):
    model = AdditionalLanguage
    fields = [
        "ietf_tag",
        "two_letter",
        "three_letter",
        "common_name",
        "native_name",
        "direction",
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


class AjaxIMBPeopleGroupListView(DataTableSourceView):
    model = IMBPeopleGroup
    fields = [
        "peid",
        "affinity_bloc",
        "people_cluster",
        "sub_continent",
        "country",
        "country_of_origin",
        "people_group",
        "population",
        "dispersed",
        "rol",
        "language",
        "religion",
        "written_scripture",
        "jesus_film",
        "radio_broadcast",
        "gospel_recording",
        "audio_scripture",
        "bible_stories"
    ]
