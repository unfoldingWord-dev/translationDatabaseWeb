from django.contrib import admin

from .models import (
    Network,
    Country,
    Language,
    Resource,
    Region,
    Media,
    Title
)


class EntryTrackingAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.source = request.user
        obj.save()


class NetworkAdmin(EntryTrackingAdmin):
    list_display = ["name"]


class CountryAdmin(EntryTrackingAdmin):
    list_display = ["code", "name", "region", "population"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("code",)
        return self.readonly_fields


class LanguageAdmin(EntryTrackingAdmin):
    list_display = ["code", "name", "gateway_language", "direction", "native_speakers"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("code",)
        return self.readonly_fields


class ResourceAdmin(EntryTrackingAdmin):
    list_display = ["title", "language", "media", "published_flag"]


class TitleAdmin(EntryTrackingAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


class MediaAdmin(EntryTrackingAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


class RegionAdmin(EntryTrackingAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(
    Network,
    NetworkAdmin
)


admin.site.register(
    Country,
    CountryAdmin
)

admin.site.register(
    Language,
    LanguageAdmin
)


admin.site.register(
    Resource,
    ResourceAdmin
)


admin.site.register(
    Region,
    RegionAdmin
)


admin.site.register(
    Title,
    TitleAdmin
)


admin.site.register(
    Media,
    MediaAdmin
)
