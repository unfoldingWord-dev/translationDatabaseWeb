import operator

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, View

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


class DataTableSourceView(View):

    @property
    def queryset(self):
        return self.model._default_manager.all()

    @property
    def search_term(self):
        return self.request.GET.get("search[value]")

    @property
    def paging_start_record(self):
        return int(self.request.GET.get("start"))

    @property
    def paging_page_length(self):
        return int(self.request.GET.get("length"))

    @property
    def order_direction(self):  # @@@ expand on this if multi-column ordering is needed
        direction = self.request.GET.get("order[0][dir]")
        if direction == "desc":
            return "-"
        return ""

    @property
    def order_field(self):  # @@@ expand on this if multi-column ordering is needed
        return self.fields[int(self.request.GET.get("order[0][column]"))]

    @property
    def current_page(self):
        return (self.paging_start_record / self.paging_page_length) + 1

    @property
    def draw(self):
        return int(self.request.GET.get("draw"))

    @property
    def filter_predicates(self):
        return [
            ("{0}__icontains".format(field), self.search_term)
            for field in self.fields
        ]

    @property
    def filtered_data(self):
        return self.queryset.filter(
            reduce(
                operator.or_,
                [Q(x) for x in self.filter_predicates]
            )
        ).order_by(
            self.order_by
        )

    @property
    def all_data(self):
        return self.queryset.all()

    @property
    def order_by(self):  # @@@ expand on this if multi-column ordering is needed
        return "{0}{1}".format(self.order_direction, self.order_field)

    @property
    def data(self):
        paginator = Paginator(self.filtered_data, self.paging_page_length, orphans=0, allow_empty_first_page=True)
        page = paginator.page(self.current_page)
        return [self.format_row(obj) for obj in page.object_list]

    def format_row(self, obj):
        row = []
        for field in self.fields:
            if hasattr(obj, "get_{0}_display".format(field)):
                row.append(getattr(obj, "get_{0}_display".format(field))())
            else:
                row.append(getattr(obj, field))
        return row

    def get(self, request, *args, **kwargs):
        return JsonResponse({
            "data": self.data,
            "draw": self.draw,
            "recordsTotal": self.all_data.count(),
            "recordsFiltered": self.filtered_data.count()
        })


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
