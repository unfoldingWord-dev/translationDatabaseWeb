from django.contrib import messages
from django.db.models import Q
# from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView
# from django.views.decorators.http import require_http_methods

from account.mixins import LoginRequiredMixin

from .models import Charter, Event
from .forms import CharterForm, EventForm
from td.utils import DataTableSourceView

import operator
import logging
logger = logging.getLogger(__name__)


# ------------------------------- #
#         DEFAULT VIEWS           #
# ------------------------------- #


class UnderConstructionView(TemplateView):
    template_name = 'tracking/under_construction.html'


# ------------------------------- #
#            HOME VIEWS           #
# ------------------------------- #

class CharterListView(TemplateView):
    template_name = 'tracking/project_list.html'


class CharterTableSourceView(DataTableSourceView):

    def __init__(self, **kwargs):
        super(CharterTableSourceView, self).__init__(**kwargs)

    @property
    def queryset(self):
        if 'pk' in self.kwargs:
            return Charter.objects.filter(language=self.kwargs['pk'])
        else:
            return self.model._default_manager.all()

    @property
    def filtered_data(self):
        if len(self.search_term) and len(self.search_term) <= 3:
            qs = self.queryset.filter(
                reduce(
                    operator.or_,
                    [Q(language__name__istartswith=self.search_term)]
                )
            ).order_by('start_date')
            if qs.count():
                return qs
        return self.queryset.filter(
            reduce(
                operator.or_,
                [Q(x) for x in self.filter_predicates]
            )
        ).order_by(
            self.order_by
        )


class AjaxCharterListView(CharterTableSourceView):
    model = Charter
    fields = [
        'language__name',
        'language__code',
        'start_date',
        'end_date',
        'contact_person'
    ]
    link_column = 'language__name'
    link_url_name = 'tracking:charter'
    link_url_field = 'pk'


# ---------------------------------- #
#            CHARTER VIEWS           #
# ---------------------------------- #


class CharterAdd(CreateView):
    model = Charter
    form_class = CharterForm

    def get_initial(self):
        return {
            'start_date': timezone.now(),
            'created_by': self.request.user.username
        }

    def form_valid(self, form):
        self.object = form.save()
        return redirect('tracking:charter_add_success', pk=self.object.id)


class CharterUpdate(LoginRequiredMixin, UpdateView):
    model = Charter
    form_class = CharterForm
    template_name_suffix = "_update_form"

    def form_valid(self, form):
        self.object = form.save()
        messages.info(self.request, "Project charter has been updated")
        return redirect('tracking:charter_add_success', pk=self.object.id)


def charter_add_success(request, pk):
    charter = get_object_or_404(Charter, pk=pk)
    context = {
        'status': 'Success',
        'charter_id': charter.id,
        'message': 'Project ' + charter.language.name + ' has been successfully added.',
    }
    return render(request, 'tracking/charter_add_success.html', context)


def charter(request, pk):
    charter = get_object_or_404(Charter, pk=pk)
    context = {'charter': charter}

    return render(request, 'tracking/charter_detail.html', context)


# -------------------------------- #
#            EVENT VIEWS           #
# -------------------------------- #


class EventAdd(CreateView):
    model = Event
    form_class = EventForm

    def get_initial(self):
        return {
            'start_date': timezone.now(),
            'created_by': self.request.user.username
        }

    def form_valid(self, form):
        self.object = form.save()
        return redirect('tracking:event_add_success', pk=self.object.id)


def event_add(request, **kwargs):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/tracking/event/add/success/')
    else:
        form = EventForm()

    context = {'form': form}

    return render(request, 'tracking/event_add.html', context)
