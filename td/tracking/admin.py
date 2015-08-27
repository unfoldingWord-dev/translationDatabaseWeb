from django.contrib import admin
from .models import Charter, Event, Material, Translator, Facilitator, Network, Department




class CharterAdmin(admin.ModelAdmin):
	fieldsets = [
		('Info', {'fields': ['language', 'countries']}),
		('Timing', {'fields': ['start_date', 'end_date']}),
		('Internal', {'fields': ['name', 'number', 'lead_dept']}),
		(None, {'fields': ['created_at', 'created_by']}),
	]
	list_display = ('language', 'start_date', 'end_date')



class EventAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['charter']}),
		(None, {'fields': ['location', 'start_date', 'end_date']}),
		(None, {'fields': ['translation_method', 'output_target']}),
		(None, {'fields': ['materials', 'tech_used', 'comp_tech_used']}),
		(None, {'fields': ['translators', 'facilitators', 'networks', 'departments']}),
		(None, {'fields': ['pub_process', 'follow_up']}),
	]
	list_display = ('charter', 'lead_dept', 'start_date', 'end_date')


admin.site.register(Charter, CharterAdmin)
admin.site.register(Event, EventAdmin)