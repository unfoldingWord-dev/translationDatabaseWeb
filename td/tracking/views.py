from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Charter, Event
from .forms import CharterForm, EventForm

import logging

logger = logging.getLogger(__name__)


#dashboard
def index(request):
	charter_list = Charter.objects.order_by('target_lang_name')
	event_list = Event.objects.order_by('charter')
	context = {
		'charter_list': charter_list,
		'event_list': event_list
	}

	return render(request, 'tracking/index.html', context);


#----------------------------------#
#           CHARTER VIEWS          #
#----------------------------------#

def charter(request, target_lang_name):
	charter = get_object_or_404(Charter, target_lang_name = target_lang_name)
	context = {'charter': charter}

	return render(request, 'tracking/charter_detail.html', context)


def charter_add(request):
	if request.method == 'POST':
		form = CharterForm(request.POST)
		if form.is_valid():
			target_lang_name = request.POST['target_lang_name']
			target_lang_ietf = request.POST['target_lang_ietf']
			gw_lang_name = request.POST['gw_lang_name']
			gw_lang_ietf = request.POST['gw_lang_ietf']
			name = request.POST['name']
			number = request.POST['number']
			start_date = request.POST['start_date']
			end_date = request.POST['end_date']
			lead_dept = request.POST['lead_dept']
			entry = Charter.objects.create(
				target_lang_name = target_lang_name,
				target_lang_ietf = target_lang_ietf,
				gw_lang_name = gw_lang_name,
				gw_lang_ietf = gw_lang_ietf,
				name = name,
				number = number,
				start_date = start_date,
				end_date = end_date,
				lead_dept = lead_dept
			)

			return HttpResponseRedirect(reverse('tracking:charter_add_success'))
	else:
		form = CharterForm()

	context = {'form': form}

	return render(request, 'tracking/charter_add.html', context)


def charter_add_success(request):
	return HttpResponse()


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