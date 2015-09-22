from django.contrib import messages
from django.db.models import Q
# from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, TemplateView
# from django.views.decorators.http import require_http_methods

from account.mixins import LoginRequiredMixin

from .models import Charter, Event
from .forms import CharterForm, EventForm
from td.utils import DataTableSourceView

import operator
import logging
logger = logging.getLogger(__name__)


# ------------------------------- #
#            HOME VIEWS           #
# ------------------------------- #


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
    # link is on column because name can't handle non-roman characters
    link_column = 'language__code'
    link_url_name = 'tracking:charter'
    link_url_field = 'pk'


# ---------------------------------- #
#            CHARTER VIEWS           #
# ---------------------------------- #


class CharterAdd(LoginRequiredMixin, CreateView):

    model = Charter
    form_class = CharterForm

    def get_initial(self):
        return {
            'start_date': timezone.now(),
            'created_by': self.request.user.username
        }

    def form_valid(self, form):
        self.object = form.save()
        return redirect('tracking:charter_add_success', obj_type='charter', pk=self.object.id)


class CharterUpdate(LoginRequiredMixin, UpdateView):
    model = Charter
    form_class = CharterForm
    template_name_suffix = "_update_form"

    def form_valid(self, form):
        self.object = form.save()
        messages.info(self.request, "Project charter has been updated")
        return redirect('tracking:charter_add_success', pk=self.object.id)


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'tracking/charter_add_success.html'

    def get(self, request, *args, **kwargs):
        # Redirects user to tracking home page if he doesn't get here from new
        #    charter or event forms
        try:
            referer = request.META['HTTP_REFERER']
        except KeyError:
            return redirect('tracking:project_list')

        allowed_urls = [
            'http://localhost:8000/tracking/charter/new/',
            'http://td.unfoldingword.org/tracking/charter/new/',
        ]

        if referer in allowed_urls:
            return super(SuccessView, self).get(self, *args, **kwargs)
        else:
            return redirect('tracking:project_list')

    def get_context_data(self, *args, **kwargs):
        # Append additional context to display custom message
        # NOTE: Maybe the logic for custom message should go in the template?
        charter = Charter.objects.get(pk=kwargs['pk'])
        context = super(SuccessView, self).get_context_data(**kwargs)
        context['link_id'] = kwargs['pk']
        if kwargs['obj_type'] == 'charter':
            context['status'] = 'Success'
            context['message'] = 'Project ' + charter.language.name + ' has been successfully added.'
        else:
            context['status'] = 'Sorry :('
            context['message'] = 'It seems like you got here by accident'
        return context


def charter(request, pk):
    charter = get_object_or_404(Charter, pk=pk)
    messages.info(request, "This page provides a link to edit a charter, but is still being worked on.")
    context = {
        'charter': charter,
    }

    return render(request, 'tracking/charter_detail.html', context)


# -------------------------------- #
#            EVENT VIEWS           #
# -------------------------------- #


def charters_autocomplete(request):
    term = request.GET.get('q').lower().encode('utf-8')
    charters = Charter.objects.filter(Q(language__code__icontains=term) | Q(language__name__icontains=term))
    data = [
        {
            'pk': charter.id,
            'ln': charter.language.ln,
            'lc': charter.language.lc,
            'lr': charter.language.lr,
            'gl': charter.language.gateway_flag
        }
        for charter in charters
    ]
    return JsonResponse({'results': data, 'count': len(data), 'term': term})


class EventAddView(CreateView):
    model = Event
    form_class = EventForm
    # success_url = ''

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
