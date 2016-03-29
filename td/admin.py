from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    AdditionalLanguage,
    TempLanguage,
    JSONData,
    Region,
    WARegion,
    Language,
    Country,
    Network,
    LanguageAltName,
    CountryEAV,
    LanguageEAV,
)
from .resources.admin import EntryTrackingAdmin


class AdditionalLanguageAdmin(EntryTrackingAdmin):
    list_display = ["ietf_tag", "common_name", "two_letter", "three_letter", "native_name", "direction", "comment",
                    "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at", "direction"]
    search_fields = ["ietf_tag", "common_name", "two_letter", "three_letter", "native_name", "comment"]


class TempLanguageAdmin(EntryTrackingAdmin):
    list_display = ["code", "lang_assigned", "status", "created_at", "modified_at"]
    list_filter = ["status", "app", "requester", "created_at", "modified_at"]
    search_fields = ["code", ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        obj.save()


class NetworkAdmin(EntryTrackingAdmin):
    list_display = ["name"]


class CountryAdmin(EntryTrackingAdmin):
    list_display = ["code", "name", "region", "wa_region", "population"]
    search_fields = ["code", "name", "region__name", "wa_region__name"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("code",)
        return self.readonly_fields


class LanguageAdmin(EntryTrackingAdmin):
    list_display = ["code", "name", "gateway_language", "direction", "native_speakers"]
    list_filter = ["gateway_flag", "country__region", "wa_region", ]
    search_fields = ["code", "name", "anglicized_name", ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("code",)
        return self.readonly_fields


# NOTE: This is superseded by  management command language_alt_names
class LanguageAltNameResource(resources.ModelResource):
    # source is needed to create LanguageEAV
    source = None

    def before_import(self, dataset, dry_run, **kwargs):
        self.source = kwargs.pop("user")
        return super(LanguageAltNameResource, self).before_import(dataset, dry_run, **kwargs)

    def skip_row(self, instance, original):
        # NOTE: This check is written because unique_together constrain on
        #    LanguageAltName doesn't seem to work to avoid duplicates. Even if
        #    it did, importing duplicates will throw an IntegrityError and
        #    aborts the import process.
        result = super(LanguageAltNameResource, self).skip_row(instance, original)
        try:
            LanguageAltName.objects.get(code=instance.code, name=instance.name)
            print "".join(["*LanguageAltName with code ", instance.code,
                           " and ", instance.name, " already exist. Skipped."])
            return True
        except LanguageAltName.DoesNotExist:
            return result

    def after_save_instance(self, instance, dry_run):
        # Avoiding double LanguageEAV creations
        if not dry_run:
            try:
                # Filter instead of get because diff langs may have the same
                #    iso-639-3 code. Specific example: 'pt' and 'pt-br'.
                for language in Language.objects.filter(iso_639_3=instance.code):
                    language.alt_name = instance
                    language.source = self.source
                    language.save()
            except Language.DoesNotExist:
                print "Language code: " + instance.code + " doesn't exist."

    class Meta:
        model = LanguageAltName
        skip_unchanged = True
        report_skipped = True
        fields = ["id", "code", "name", ]


class LanguageAltNameAdmin(EntryTrackingAdmin, ImportExportModelAdmin):
    resource_class = LanguageAltNameResource
    list_display = ["code", "name", ]
    search_fields = ["code", "name", ]


class RegionAdmin(EntryTrackingAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ["name"]}


class LanguageEAVAdmin(EntryTrackingAdmin):
    list_display = ["entity", "attribute", "value", "source_ct", "source_id"]
    list_filter = ["attribute", "source_ct", ]


class CountryEAVAdmin(EntryTrackingAdmin):
    list_display = ["entity", "attribute", "value", "source_ct", "source_id"]
    list_filter = ["attribute", "source_ct", ]


admin.site.register(AdditionalLanguage, AdditionalLanguageAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(LanguageAltName, LanguageAltNameAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(WARegion)
admin.site.register(JSONData)
admin.site.register(CountryEAV, CountryEAVAdmin)
admin.site.register(LanguageEAV, LanguageEAVAdmin)
admin.site.register(TempLanguage, TempLanguageAdmin)
