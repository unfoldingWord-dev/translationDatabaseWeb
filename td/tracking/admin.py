from django.contrib import admin
from .models import Charter, Event, Material, Translator, Facilitator, Department


class CharterAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Info', {'fields': ['language', 'countries']}),
        ('Timing', {'fields': ['start_date', 'end_date']}),
        ('Internal', {'fields': ['number', 'lead_dept', 'contact_person']}),
        (None, {'fields': ['created_at', 'created_by']}),
    ]
    list_display = ('language', 'start_date', 'end_date')


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['charter']}),
        (None, {'fields': ['location', 'start_date', 'end_date']}),
        (None, {'fields': ['translation_method', 'output_target']}),
        (None, {'fields': ['materials', 'tech_used', 'comp_tech_used']}),
        (None, {'fields': ['translators', 'facilitators', 'departments']}),
        (None, {'fields': ['pub_process', 'follow_up']}),
    ]
    list_display = ('charter', 'old_lead_dept', 'start_date', 'end_date')


admin.site.register(Charter, CharterAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Department)
admin.site.register(Material)
admin.site.register(Translator)
admin.site.register(Facilitator)
