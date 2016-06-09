from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from td.gl_tracking.models import Partner
from .models import (
    Charter,
    Department,
    Event,
    Facilitator,
    Hardware,
    Material,
    Output,
    Publication,
    Software,
    Translator,
    TranslationMethod,
)
from td.models import Language


class CharterResource(resources.ModelResource):
    language = fields.Field(column_name="language_code", attribute="language",
                            widget=widgets.ForeignKeyWidget(Language, "code"))
    lead_dept = fields.Field(column_name="lead_dept_name", attribute="lead_dept",
                             widget=widgets.ForeignKeyWidget(Department, "name"))
    partner = fields.Field(column_name="partner_name", attribute="partner",
                           widget=widgets.ForeignKeyWidget(Partner, "name"))

    def before_import(self, dataset, dry_run, **kwargs):
        for name in dataset["created_by"]:
            name = name.title()
        return super(CharterResource, self).before_import(dataset, dry_run, **kwargs)

    class Meta:
        model = Charter
        fields = ("id", "language", "start_date", "end_date", "lead_dept", "contact_person", "new_start", "partner",
                  "created_by")


class EventResource(resources.ModelResource):

    class Meta:
        model = Event
        fields = ('id', 'charter', 'number', 'location', 'start_date', 'end_date', 'lead_dept', 'output_target', 'publication', 'current_check_level', 'target_check_level', 'translation_methods', 'software', 'hardware', 'contact_person', 'materials', 'translators', 'facilitators', 'networks', 'departments', 'created_at', 'created_by')


class CharterAdmin(ImportExportModelAdmin):
    resource_class = CharterResource
    fieldsets = [
        ("General", {"fields": ["language", "countries", "new_start"]}),
        ("Timing", {"fields": [("start_date", "end_date")]}),
        ("Internal", {"fields": ["number", "lead_dept", "contact_person", "partner"]}),
        ("Submission Info", {"fields": [("created_at", "created_by"), ("modified_at", "modified_by")]}),
    ]
    filter_horizontal = ('countries', )
    list_display = ("language", "__unicode__", "start_date", "end_date", "number", "contact_person")


class EventAdmin(ImportExportModelAdmin):
    resource_class = EventResource
    fieldsets = [
        ("General", {"fields": (("charter", "number"), "location", ("start_date", "end_date"), "lead_dept", "contact_person")}),
        ("Parties Involved", {"fields": ["translators", "facilitators", "departments", "networks", "partner"]}),
        ("Resources", {"fields": ["software", "hardware", "translation_methods", "materials"]}),
        ("Misc", {"fields": ["output_target", "publication", "current_check_level", "target_check_level", "comment"]}),
        ("Submission Info", {"fields": [("created_at", "created_by"), ("modified_at", "modified_by")]}),
    ]
    filter_horizontal = ('translators', 'networks', )
    list_display = ("charter", "number", "location", "start_date", "end_date", "contact_person")


admin.site.register(Charter, CharterAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Department)
admin.site.register(Material)
admin.site.register(Translator)
admin.site.register(Facilitator)
admin.site.register(TranslationMethod)
admin.site.register(Software)
admin.site.register(Hardware)
admin.site.register(Output)
admin.site.register(Publication)
