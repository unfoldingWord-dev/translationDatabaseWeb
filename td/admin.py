from django.contrib import admin

from .models import AdditionalLanguage, Region, Language, Country, Network
from td.resources.admin import EntryTrackingAdmin

admin.site.register(
    AdditionalLanguage,
    list_display=[
        "ietf_tag",
        "common_name",
        "two_letter",
        "three_letter",
        "native_name",
        "direction",
        "comment",
        "created_at",
        "updated_at",
    ],
    list_filter=[
        "created_at",
        "updated_at"
    ],
    search_fields=[
        "ietf_tag",
        "comment_name",
        "comment"
    ]
)


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
    Region,
    RegionAdmin
)
