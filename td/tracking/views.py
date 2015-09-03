from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib import messages

from account.mixins import LoginRequiredMixin

from .models import Charter, Event
from .forms import CharterForm, EventForm

import logging

logger = logging.getLogger(__name__)


#dashboard
def index(request):
	charter_list = Charter.objects.order_by('language')
	event_list = Event.objects.order_by('charter')
	context = {
		'charter_list': charter_list,
		'event_list': event_list
	}

	return render(request, 'tracking/index.html', context);


#----------------------------------#
#           CHARTER VIEWS          #
#----------------------------------#

def charter(request, pk):
	charter = get_object_or_404(Charter, pk = pk)
	context = {'charter': charter}

	return render(request, 'tracking/charter_detail.html', context)


class charter_add(CreateView):
	model = Charter
	form_class = CharterForm

	def get_initial(self):
		return {
			'start_date': timezone.now(),
			'end_date': None,
			'created_by': self.request.user.username
		}

	def form_valid(self, form):
		self.object = form.save()
		messages.info(self.request, "Project charter has been added")
		return redirect('tracking:charter_add_success')

class charter_update(LoginRequiredMixin, UpdateView):
	model = Charter
	form_class = CharterForm
	template_name_suffix = "_update_form"

	def form_valid(self, form):
		self.object = form.save()
		messages.info(self.request, "Project charter has been updated")
		return redirect('tracking:charter_add_success')


def charter_add_success(request):
	return HttpResponse('Project has been successfully created')


#--------------------------------#
#           EVENT VIEWS          #
#--------------------------------#

def event(request, event_id):
	event = get_object_or_404(Event, id = event_id)
	context = {'event': event}

	return render(request, 'tracking/event_detail.html', context)


def event_add(request):
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/tracking/event/add/success/')
	else:
		form = EventForm()

	context = {'form': form}

	return render(request, 'tracking/event_add.html', context)