import calendar
import operator
import types

from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.views.generic import View
from django.template import Variable, VariableDoesNotExist
from django.core.urlresolvers import reverse

from xml.dom import minidom
from svglib.svglib import SvgRenderer
from reportlab.graphics import renderPDF

from .models import WARegion, Country, Language
from td.tracking.models import Event


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


def get_event_total(start=None, end=None, regions=None):
    """
    Total the number of events started for a given range.
    :param start: Date string. Marks the beginning of the range. Defaults to Oct 1 of the previous year.
    :param end: Date string. Marks the end of the range. Defaults to Sep 30 of the current year.
    :param regions: List of WARegion or Region instances. Defaults to all WA region.
    :return: A list of dictionaries that contain "text", and "count" info for each WA region.
    """
    start = start or datetime(datetime.now().year - 1, 10, 1).strftime("%Y-%m-%d")
    end = end or datetime(datetime.now().year, 9, 30).strftime("%Y-m-%d")
    regions = regions or WARegion.objects.all()
    try:
        # Get the counts for events started in a given range for each region
        events = Event.objects.filter(start_date__range=(start, end))
        total_count = [
            {"text": region.name, "count": events.filter(charter__language__wa_region__slug=region.slug).count()}
            for region in regions
        ]
        # Attach the total to the head of the list
        total_count.insert(0, {"text": "Total", "count": events.count()})
    except TypeError:
        total_count = []
    return total_count


def get_event_count_data(mode="dashboard", option="overall", fy=0):
    """
    Construct and return rows of data to be displayed by an event-count table
    :param mode: Determines what objects are going to be the table entry. For example, "dashboard" mode means that the
        table is going to display a list of all WA regions, while, in "region" mode, it will list all the countries in a
        region. It defaults to "dashboard".
    :param option: The selected option from the <select name="option"> in _event_count_form.html
    :param fy: The number of year that should be added to the current fiscal year. 0 for the current financial year,
        1 for the next, -1 for the last, 3 for three financial years ahead, etc. This will be scope the search.
    :return: A two-dimensional list that represent the whole data table, with each second-dimension list represents a
        row in the table.
    """
    obj_list = WARegion.objects.all() if mode == "dashboard" and option == "overall"\
        else WARegion.objects.get(slug__iexact=option).country_set.all() if mode == "dashboard" and option != "overall"\
        else WARegion.objects.get(slug__iexact=option).country_set.all() if mode == "region"\
        else Country.objects.get(code__iexact=option).language_set.all() if mode == "country"\
        else Language.objects.filter(code__iexact=option) if mode == "language"\
        else []
    fiscal_year = get_wa_fy(datetime.now().date().year + int(fy))
    data = []

    for x in obj_list:
        # Create a row that contains just the monthly counts
        term = x.slug if isinstance(x, WARegion) else x.code
        row = [
            _get_monthly_count(fiscal_year.get("full_year"), month, x, term.lower())
            for month in range(10, 13) + range(1, 10)
        ]
        # Add the total of monthly counts to the end of the row
        row.append(sum(row))
        # Add the appropriate object name and link to the beginning of the row
        row.insert(0, mark_safe("<a href=\"" + x.get_absolute_url() + "\">" + x.name + "</a>"))
        # Register the finalized row entry
        data.append(row)

    return data


def _get_monthly_count(fy, month, obj, term):
    """
    Calculate the number of events started in a month.
    :param fy: The fiscal year as a scope for the search
    :param month: The month of which to get the count
    :param mode: "dashboard", "region", "country", or "language"
    :param term: The search term: Country code, language code, or WA Region'slug.
    :return: The number of events started in a given month, or 0 if mode is not recognized.
    """
    # Since WA financial year spans more than one calendar year, set the year back by one to get the start of the given
    # financial year if the month in question is October, November, or December.
    year = int(fy) - 1 if 10 <= month <= 12 else fy
    # Get the end date of a month (28, 29, 30, or 31)
    _, end_date = calendar.monthrange(int(year), int(month))
    # Assemble the range
    month_start = "-".join([str(year), str(month), "1"])
    month_end = "-".join([str(year), str(month), str(end_date)])
    # Return the count based on the designated range, model, and term.
    events = Event.objects.filter(start_date__range=(month_start, month_end))
    result = events.filter(charter__language__code__iexact=term).count() if isinstance(obj, Language)\
        else events.filter(charter__language__country__code__iexact=term).count() if isinstance(obj, Country)\
        else events.filter(charter__language__wa_region__slug__iexact=term).count() if isinstance(obj, WARegion)\
        else 0
    return result


def get_total_by_month(data):
    """
    Return a row of total (by column) to be used in the footer of a data table.
    :param data: A two-dimensional list that represents the data table
    :return: A list of integers, which are the result of adding the values in each column of each row. For example, if
        [["title1", a, b, c], ["title2", d, e, f]] were passed in, the return value will be [a+d, b+e, c+f].
    """
    # If initializer is not provided and there's only one row in data, zipped_reduced.pop(0) will, somehow, affect
    # context["data"] - making it lose index 0 as well.
    initializer = ["", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    zipped_reduced = reduce(lambda row_1, row_2: zip(row_1, row_2), data, initializer)
    zipped_reduced[0] = "Total"
    return [reduce(lambda a, b: int(a) + int(b), flatten_tuple(t)) for t in zipped_reduced]


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
                                str(v).encode("utf-8")
                            ))
                        else:
                            row.append('<a href="{0}">{1}</a>'.format(reverse(
                                self.link_url_name,
                                kwargs={self.link_url_field: getattr(obj, self.link_url_field)}),
                                str(v).encode("utf-8")
                            ))
                    else:
                        row.append(v)
        return row

    def get(self, request, *args, **kwargs):
        return JsonResponse({
            "data": self.data,
            "draw": self.draw,
            "recordsTotal": self.all_data.count(),
            "recordsFiltered": self.filtered_data.count()
        })
