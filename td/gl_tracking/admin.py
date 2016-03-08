from django.contrib import admin

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin
from import_widgets import NullableForeignKeyWidget

from td.models import Language, Country
from td.gl_tracking.models import Phase, DocumentCategory, Document, Progress, Partner, Method, GLDirector


class PhaseAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "description")


class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "phase")


class DocumentAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "description", "category")
    list_filter = ("category", )


class ProgressResource(resources.ModelResource):
    language = fields.Field("language", "language", widgets.ForeignKeyWidget(Language, "code"), None)
    type = fields.Field("type", "type", widgets.ForeignKeyWidget(Document, "code"), None)
    methods = fields.Field("methods", "methods", widgets.ManyToManyWidget(Method, ",", "name"), None)
    partners = fields.Field("partners", "partners", widgets.ManyToManyWidget(Partner, ",", "name"), None)

    class Meta:
        model = Progress
        fields = ("id", "language", "type", "is_online", "methods", "completion_rate", "completion_date", "qa_level",
                  "in_door43", "in_uw", "partners", "notes", "is_done")


class ProgressAdmin(ImportExportModelAdmin):
    resource_class = ProgressResource
    list_display = ("type", "language", "completion_rate", "completion_date", "notes", )
    list_filter = ("type", "language", "completion_rate", "completion_date", )


class GLDirectorAdmin(admin.ModelAdmin):
    list_display = ("user", "regions_string")
    list_filter = ("regions", )

    def regions_string(self, obj):
        return ", ".join([r.slug for r in obj.regions.all()])

    regions_string.admin_order_field = "user__username"


class PartnerResource(resources.ModelResource):
    country = fields.Field("country", "country", NullableForeignKeyWidget(Country, "name"), None)

    class Meta:
        model = Partner
        fields = ("id", "name", "country", "city", "province")
        report_skipped = True


class PartnerAdmin(ImportExportModelAdmin):
    resource_class = PartnerResource
    list_display = ("name", "country", "city", "is_active")

admin.site.register(Phase, PhaseAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Method)
admin.site.register(GLDirector, GLDirectorAdmin)
