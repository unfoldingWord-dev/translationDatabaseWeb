from django.contrib import admin

from td.gl_tracking.models import Phase, DocumentCategory, Document, Progress, Partner


class PhaseAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "description")


class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "phase")


class DocumentAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "description", "category")


class ProgressAdmin(admin.ModelAdmin):
    list_display = ("type", "language", "completion_rate", "completion_date", "notes")


admin.site.register(Phase, PhaseAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(Partner)
