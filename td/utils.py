import operator

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import View


def str_to_bool(value, allow_null=False):
    if str(value).strip().lower() in ["yes", "true", "1", "y"]:
        return True
    if allow_null and str(value).strip().lower() in ["no", "n", "false", "0"]:
        return False
    elif allow_null:
        return None
    else:
        return False


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
