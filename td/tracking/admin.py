from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

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
from td.models import Language, Country


class CharterResource(resources.ModelResource):

    def before_import(self, dataset, dry_run, **kwargs):
        language_ids = []
        lead_dept_ids = []
        country_ids = []
        for language in dataset["language_code"]:
            language_ids.append(Language.objects.get(code=language).id)
        for dept in dataset["lead_dept_name"]:
            lead_dept_ids.append(Department.objects.get(name=dept).id)
        for countries in dataset["country_codes"]:
            ids = []
            codes = countries.split(",")
            for code in codes:
                ids.append(str(Country.objects.get(code=code).id))
            country_ids.append(",".join(ids))
        dataset.insert_col(1, language_ids, "language")
        dataset.insert_col(7, lead_dept_ids, "lead_dept")
        dataset.insert_col(3, country_ids, "countries")
        return super(CharterResource, self).before_import(dataset, dry_run, **kwargs)

    class Meta:
        model = Charter
        fields = ('id', 'language', 'countries', 'start_date', 'end_date', 'lead_dept', 'number', 'contact_person', 'created_by')


class CharterAdmin(ImportExportModelAdmin):
    resource_class = CharterResource
    fieldsets = [
        ("General", {"fields": ["language", "countries"]}),
        ("Timing", {"fields": [("start_date", "end_date")]}),
        ("Internal", {"fields": ["number", "lead_dept", "contact_person"]}),
        ("Submission Info", {"fields": [("created_at", "created_by")]}),
    ]
    filter_horizontal = ('countries', )
    list_display = ("language", "__unicode__", "start_date", "end_date", "number", "contact_person")


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General", {"fields": (("charter", "number"), "location", ("start_date", "end_date"), "lead_dept", "contact_person")}),
        ("Parties Involved", {"fields": ["translators", "facilitators", "departments", "networks"]}),
        ("Resources", {"fields": ["software", "hardware", "translation_methods", "materials"]}),
        ("Misc", {"fields": ["output_target", "publication", "current_check_level", "target_check_level"]}),
        ("Submission Info", {"fields": [("created_at", "created_by")]}),
    ]
    filter_vertical = ('translators', 'networks', )
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
