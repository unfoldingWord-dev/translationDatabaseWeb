from django.contrib import admin
from .models import Charter, Event, Material, Translator, Facilitator, Network, Department




class CharterAdmin(admin.ModelAdmin):
	fieldsets = [
		('Language Info', {'fields': ['target_lang_name', 'target_lang_ietf', 'gw_lang_name', 'gw_lang_ietf', 'countries']}),
		('Timing Info', {'fields': ['start_date', 'end_date']}),
		(None, {'fields': ['name', 'number']}),
		(None, {'fields': ['lead_dept']}),
	]
	list_display = ('name', 'gw_lang_name', 'start_date', 'end_date')

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