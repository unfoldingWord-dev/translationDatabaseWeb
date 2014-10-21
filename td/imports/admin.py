from django.contrib import admin

from .models import (
    EthnologueCountryCode,
    EthnologueLanguageCode,
    EthnologueLanguageIndex,
    SIL_ISO_639_3,
    WikipediaISOLanguage
)


class LockedDownModelAdmin(admin.ModelAdmin):

    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def save_model(self, request, obj, form, change):
        pass


class EthnologueCountryCodeAdmin(LockedDownModelAdmin):
    list_display = ["code", "name", "area", "date_imported"]
    list_filter = ["area"]
    search_fields = ["code", "name", "area"]


class EthnologueLanguageCodeAdmin(LockedDownModelAdmin):
    list_display = ["code", "country_code", "status", "name", "date_imported"]
    list_filter = ["country_code", "status"]
    search_fields = ["code", "name"]


class EthnologueLanguageIndexAdmin(LockedDownModelAdmin):
    list_display = ["language_code", "country_code", "name_type", "name", "date_imported"]
    list_filter = ["name_type", "country_code"]
    search_fields = ["language_code", "name"]


class WikipediaISOLanguageAdmin(LockedDownModelAdmin):
    list_display = [
        "language_family",
        "language_name",
        "native_name",
        "iso_639_1",
        "iso_639_2t",
        "iso_639_2b",
        "iso_639_3",
        "iso_639_9",
        "notes",
        "date_imported"
    ]
    list_filter = ["language_family"]
    search_fields = ["language_name", "native_name", "notes"]


class SIL_ISO_639_3Admin(LockedDownModelAdmin):
    list_display = [
        "code",
        "part_2b",
        "part_2t",
        "part_1",
        "scope",
        "language_type",
        "ref_name",
        "comment",
        "date_imported",
    ]
    list_filter = ["scope", "language_type"]
    search_fields = ["code", "part_1", "comment", "ref_name"]


admin.site.register(EthnologueCountryCode, EthnologueCountryCodeAdmin)
admin.site.register(EthnologueLanguageCode, EthnologueLanguageCodeAdmin)
admin.site.register(EthnologueLanguageIndex, EthnologueLanguageIndexAdmin)
admin.site.register(WikipediaISOLanguage, WikipediaISOLanguageAdmin)
admin.site.register(SIL_ISO_639_3, SIL_ISO_639_3Admin)
