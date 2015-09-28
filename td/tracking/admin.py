from django.contrib import admin
from .models import (
    Charter,
    Event,
    Material,
    Translator,
    Facilitator,
    Department,
    TranslationService,
    Software,
    Hardware,
)


class CharterAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Info", {"fields": ["language", "countries"]}),
        ("Timing", {"fields": ["start_date", "end_date"]}),
        ("Internal", {"fields": ["number", "lead_dept", "contact_person"]}),
        (None, {"fields": ["created_at", "created_by"]}),
    ]
    list_display = ("language", "__unicode__", "start_date", "end_date", "number", "contact_person")


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["charter"]}),
        (None, {"fields": ["location", "start_date", "end_date"]}),
        (None, {"fields": ["translation_services", "output_target"]}),
        (None, {"fields": ["materials", "software", "hardware"]}),
        (None, {"fields": ["translators", "facilitators", "lead_dept", "departments"]}),
        (None, {"fields": ["publishing_process", "contact_person"]}),
    ]
    list_display = ("charter", "lead_dept", "start_date", "end_date")


admin.site.register(Charter, CharterAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Department)
admin.site.register(Material)
admin.site.register(Translator)
admin.site.register(Facilitator)
admin.site.register(TranslationService)
admin.site.register(Software)
admin.site.register(Hardware)
