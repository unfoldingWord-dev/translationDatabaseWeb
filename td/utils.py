import operator
import types

from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import View
from django.template import Variable, VariableDoesNotExist
from django.core.urlresolvers import reverse

from xml.dom import minidom
from svglib.svglib import SvgRenderer
from reportlab.graphics import renderPDF


def str_to_bool(value, allow_null=False):
    if str(value).strip().lower() in ["yes", "true", "1", "y"]:
        return True
    if allow_null and str(value).strip().lower() in ["no", "n", "false", "0"]:
        return False
    elif allow_null:
        return None
    else:
        return False


def svg_to_pdf(svg_data):
    svgr = SvgRenderer()
    doc = minidom.parseString(svg_data.encode("utf-8"))
    svgr.render(doc.documentElement)
    drawing = svgr.finish()
    pdf = renderPDF.drawToString(drawing)
    return pdf


def flatten_tuple(t):
    """Return a flat tuple."""
    if not isinstance(t, types.TupleType):
        return (t, )
    elif len(t) == 0:
        return ()
    else:
        return flatten_tuple(t[0]) + flatten_tuple(t[1:])


def get_wa_fy(year=None, month=None):
    """
    Parse a given year and/or month onto a dictionary containing info about the fiscal year.
    :param year: Year to be parsed
    :param month: Month to be parsed
    :return: A dictionary that contains "year", "full_year", "current_start", and "current_end" of the financial year.
    """
    month = month or datetime.now().date().month
    year = year or datetime.now().date().year
    if month >= 10:
        year += 1
    return {
        "year": str(year)[-2:],
        "full_year": str(year),
        "current_start": str(year - 1) + "-10-1",
        "current_end": str(year) + "-9-30"
    }


def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


def two_digit_datetime(d):
    return "".join(["0", d])[-2:]


class DataTableSourceView(View):

    def __init__(self, **kwargs):
        super(DataTableSourceView, self).__init__(**kwargs)

    @property
    def queryset(self):
        return self.model.objects.all()

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
        model_fields = [l.name for l in self.model._meta.fields if hasattr(l, "name")]
        return [
            ("{0}__icontains".format(field), self.search_term)
            for field in self.fields if field.split("__")[0] in model_fields
        ]

    @property
    def filtered_data(self):
        return self.queryset.filter(
            reduce(operator.or_, [Q(x) for x in self.filter_predicates])
        ).order_by(self.order_by)

    @property
    def all_data(self):
        return self.queryset.all()

    @property
    def order_by(self):  # @@@ expand on this if multi-column ordering is needed
        return "{0}{1}".format(self.order_direction, self.order_field)

    @property
    def data(self):
        obj_list = Paginator(self.filtered_data, self.paging_page_length, orphans=0, allow_empty_first_page=True)\
            .page(self.current_page).object_list if self.paging_page_length >= 0 else self.filtered_data
        return [self.format_row(obj) for obj in obj_list]

    def format_row(self, obj):
        row = []
        for field in self.fields:
            if hasattr(obj, "get_{0}_display".format(field)):
                row.append(getattr(obj, "get_{0}_display".format(field))())
            else:
                try:
                    var = Variable("obj.{0}".format(field.replace("__", ".")))
                    v = var.resolve({"obj": obj})
                except VariableDoesNotExist:
                    v = None
                if isinstance(v, bool):
                    if v:
                        row.append('<i class="fa fa-check text-success"></i>')
                    else:
                        row.append('<i class="fa fa-times text-danger"></i>')
                else:
                    if hasattr(self, "link_column") and self.link_column == field:
                        # NOTE: Added if statement and the first conditional code to make this work with linking project
                        #    list to language detail. The problems with the original one (under else) are:
                        #    1. Charter model has 'lang_id' attribute that gets the related language's pk, but then the
                        #       reverse() finds no match since 'uw/language_detail/' looks for a "pk" as an argument,
                        #       not a "lang_id".
                        #    2. Charter model should not have more than one "pk" as attributes (one refers to itself,
                        #       one refers to the related language's pk)
                        #   Solution:
                        #       1. Rename the kwargs key to "pk" if the link_url_field is "lang_id"
                        # NOTE by Vicky Leong, 10.12.15
                        if (self.link_url_field == "lang_id"):
                            row.append('<a href="{0}">{1}</a>'.format(reverse(
                                self.link_url_name,
                                kwargs={"pk": getattr(obj, self.link_url_field)}),
                                v.encode("utf-8") if hasattr(v, "encode") else v
                            ))
                        else:
                            row.append('<a href="{0}">{1}</a>'.format(reverse(
                                self.link_url_name,
                                kwargs={self.link_url_field: getattr(obj, self.link_url_field)}),
                                v.encode("utf-8") if hasattr(v, "encode") else v
                            ))
                    else:
                        row.append(v)
        return row

    def get(self, request, *args, **kwargs):
        # type: (object, object, object) -> object
        return JsonResponse({
            "data": self.data,
            "draw": self.draw,
            "recordsTotal": self.all_data.count(),
            "recordsFiltered": self.filtered_data.count()
        })
