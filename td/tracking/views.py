from django.shortcuts import render
from django.http import HttpResponse

from .models import Charter, Event


#dashboard
def index(request):
	charter_list = Charter.objects.order_by('-proj_num')
	event_list = Event.objects.order_by('-charter')
	context = {
		'charter_list': charter_list,
		'event_list': event_list
	}

	return render(request, 'tracking/index.html', context);


def charter(request, proj_num):
	try:
		charter = Charter.objects.get(proj_num = proj_num)
		context = {'charter': charter}
	except Charter.DoesNotExist:
		raise Http404('Charter record not found')
	return render(request, 'tracking/charter.html', context)


def event(request, event_id):
	try:
		event = Charter.objects.get(id = event_id)
		context = {'event': event}
	except Event.DoesNotExist:
		raise Http404('Event record not found')
	return render(request, 'tracking/event.html', context)


def charter_add(request):
	return HttpResponse("Add a new project charter %s" % request)


def charter_added(request):
	return HttpResponse("Project charter is added %s" % request)


def event_add(request):
	return HttpResponse("Add a new project event %s" % request)


def event_added(request):
	return HttpResponse("Project event is added %s" % request)