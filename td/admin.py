from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    AdditionalLanguage,
    Region,
    WARegion,
    Language,
    Country,
    Network,
    LanguageAltName,
    CountryEAV,
    LanguageEAV,
)
from td.resources.admin import EntryTrackingAdmin


class AdditionalLanguageAdmin(EntryTrackingAdmin):
    list_display = ["ietf_tag", "common_name", "two_letter", "three_letter",
                    "native_name", "direction", "comment", "created_at",
                    "updated_at", ]
    list_filter = ["created_at", "updated_at", ]
    search_fields = ["ietf_tag", "comment_name", "comment", ]


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
    list_filter = ["gateway_flag", "country__region", "wa_region", ]
    search_fields = ["code", "name", "anglicized_name", ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("code",)
        return self.readonly_fields


class LanguageAltNameResource(resources.ModelResource):
    # source is needed to create LanguageEAV
    source = None

    def before_import(self, dataset, dry_run, **kwargs):
        # Get the username from the first entry in the extra column on the CSV
        self.source = User.objects.get(username=dataset["username"][0])
        return super(LanguageAltNameResource, self).before_import(dataset, dry_run, **kwargs)

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
admin.site.register(CountryEAV, CountryEAVAdmin)
admin.site.register(LanguageEAV, LanguageEAVAdmin)
