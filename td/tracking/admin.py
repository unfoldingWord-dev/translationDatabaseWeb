from django.contrib import admin

from .models import (
    Charter,
    Department,
    Event,
    Facilitator,
    Hardware,
    Material,
    Software,
    Translator,
    TranslationService,
)


class CharterAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Info", {"fields": ["language", "countries"]}),
        ("Timing", {"fields": ["start_date", "end_date"]}),
        ("Internal", {"fields": ["number", "lead_dept", "contact_person"]}),
        ("Submission Info", {"fields": ["created_at", "created_by"]}),
    ]
    list_display = ("language", "__unicode__", "start_date", "end_date", "number", "contact_person")


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General Info", {"fields": (("charter", "number"), "location", ("start_date", "end_date"), "lead_dept", "contact_person")}),
        ("Parties Involved", {"fields": ["translators", "facilitators", "departments", "networks"]}),
        ("Resources", {"fields": ["software", "hardware", "translation_services", "materials"]}),
        (None, {"fields": ["output_target", "publishing_process"]}),
        ("Submission Info", {"fields": ["created_at", "created_by"]}),
    ]
    list_display = ("charter", "number", "location", "start_date", "end_date", "contact_person")


admin.site.register(Charter, CharterAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Department)
admin.site.register(Material)
admin.site.register(Translator)
admin.site.register(Facilitator)
admin.site.register(TranslationService)
admin.site.register(Software)
admin.site.register(Hardware)
