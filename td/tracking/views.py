from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	return HttpResponse("Tracking Index %s" % request);

def add_charter(request):
	return HttpResponse("Add a new project charter %s" % request)

def add_event(request):
	return HttpResponse("Add a new project event %s" % request)

def charter_added(request):
	return HttpResponse("Project charter is added %s" % request)

def event_added(request):
	return HttpResponse("Project event is added %s" % request)