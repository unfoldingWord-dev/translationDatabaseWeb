from django.contrib import admin
from .models import Charter, Event, Material, Translator, Facilitator




class CharterAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['proj_num']}),
		('Timing Info', {'fields': ['start_date', 'end_date']}),
		('Language Info', {'fields': ['lang_name', 'lang_ietf', 'gw_lang_name', 'gw_lang_ietf']}),
		(None, {'fields': ['lead_dept']}),
	]
	list_display = ('proj_num', 'lang_name', 'gw_lang_name', 'start_date', 'end_date')


class MaterialInline(admin.TabularInline):
	model = Material
	extra = 1

class TranslatorInline(admin.TabularInline):
	model = Translator
	extra = 1

class FacilitatorInline(admin.TabularInline):
	model = Facilitator
	extra = 1

class EventAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['charter']}),
		(None, {'fields': ['location', 'start_date', 'end_date']}),
		(None, {'fields': ['translation_method', 'output_target']}),
		(None, {'fields': ['tech_used', 'comp_tech_used']}),
		(None, {'fields': ['pub_process', 'follow_up']}),
	]
	inlines = [MaterialInline, TranslatorInline, FacilitatorInline]
	list_display = ('charter', 'lead_dept', 'start_date', 'end_date')


admin.site.register(Charter, CharterAdmin)
admin.site.register(Event, EventAdmin)