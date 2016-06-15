import calendar
from datetime import datetime

from django.utils.safestring import mark_safe

from td.models import WARegion, Country, Language
from td.tracking.models import Event
from td.utils import get_wa_fy, flatten_tuple


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
    :param obj: "dashboard", "region", "country", or "language"
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
