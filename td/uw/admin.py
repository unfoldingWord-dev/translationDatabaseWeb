from django.contrib import admin

from .models import (
    Network,
    BibleContent,
    Country,
    Language,
    Translator,
    Organization,
    WorkInProgress,
    Scripture,
    TranslationNeed,
    Resource
)


class EntryTrackingAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.source = request.user
        obj.save()


class NetworkAdmin(EntryTrackingAdmin):
    list_display = ["name"]


class BibleContentAdmin(EntryTrackingAdmin):
    list_display = ["name"]


class CountryAdmin(EntryTrackingAdmin):
    list_display = ["code", "name", "area", "population"]


class LanguageAdmin(EntryTrackingAdmin):
    list_display = ["code", "name", "gateway_language", "native_speakers"]


class TranslatorAdmin(EntryTrackingAdmin):
    list_display = ["name", "email", "d43username", "location", "phone", "relationship", "other"]


class OrganizationAdmin(EntryTrackingAdmin):
    list_display = ["name", "email", "d43username", "location", "phone"]


class WorkInProgressAdmin(EntryTrackingAdmin):
    list_display = ["kind", "language", "bible_content", "paradigm", "anticipated_completion_date"]


class ScriptureAdmin(EntryTrackingAdmin):
    list_display = ["kind", "language", "bible_content", "year", "publisher"]


class TranslationNeedAdmin(EntryTrackingAdmin):
    list_display = ["language", "text_gaps", "text_updates", "other_gaps", "other_updates"]


class ResourceAdmin(EntryTrackingAdmin):
    list_display = ["language", "name", "copyright", "copyright_holder", "license"]


admin.site.register(
    Network,
    NetworkAdmin
)

admin.site.register(
    BibleContent,
    BibleContentAdmin
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
    Translator,
    TranslatorAdmin
)

admin.site.register(
    Organization,
    OrganizationAdmin
)

admin.site.register(
    WorkInProgress,
    WorkInProgressAdmin
)

admin.site.register(
    Scripture,
    ScriptureAdmin
)

admin.site.register(
    TranslationNeed,
    TranslationNeedAdmin
)

admin.site.register(
    Resource,
    ResourceAdmin
)
