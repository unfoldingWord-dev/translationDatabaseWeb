from django.contrib import admin

from .models import (
    Resource,
    Media,
    Title
)


class EntryTrackingAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.source = request.user
        obj.save()


class ResourceAdmin(EntryTrackingAdmin):
    list_display = ["title", "language", "published_flag"]


class TitleAdmin(EntryTrackingAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


class MediaAdmin(EntryTrackingAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(
    Resource,
    ResourceAdmin
)


admin.site.register(
    Title,
    TitleAdmin
)


admin.site.register(
    Media,
    MediaAdmin
)
