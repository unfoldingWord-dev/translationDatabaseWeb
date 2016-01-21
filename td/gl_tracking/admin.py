from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from td.models import Language
from td.gl_tracking.models import Phase, DocumentCategory, Document, Progress, Partner, RegionalDirector, Method


class PhaseAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "description")


class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "phase")


class DocumentAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "description", "category")


class ProgressResource(resources.ModelResource):

    def before_import(self, dataset, dry_run, **kwargs):
        language_ids = []
        type_ids = []
        # date_objs = []
        for code in dataset["language_code"]:
            print '\nLANGUAGE: ', code
            language_ids.append(Language.objects.get(code=code).id)
        for doc in dataset["document_slug"]:
            print '\nDOCUMENT: ', doc
            type_ids.append(Document.objects.get(code=doc).id)
        dataset.insert_col(1, language_ids, "language")
        dataset.insert_col(2, type_ids, "type")
        return super(ProgressResource, self).before_import(dataset, dry_run, **kwargs)

    class Meta:
        model = Progress
        fields = ('id', 'language', 'type', 'completion_rate', 'completion_date', 'is_online', 'in_door43', 'in_uw', 'notes', 'is_done')


class ProgressAdmin(ImportExportModelAdmin):
    resource_class = ProgressResource
    list_display = ("type", "language", "completion_rate", "completion_date", "notes")


class RegionalDirectorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "middle_name", "last_name", "user")


admin.site.register(Phase, PhaseAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(Partner)
admin.site.register(RegionalDirector, RegionalDirectorAdmin)
admin.site.register(Method)