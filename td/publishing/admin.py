from django.db.models import Q

from django.contrib import admin

import reversion

from .models import (
    Contact,
    Organization,
    Connection,
    ConnectionType,
    RecentCommunication,
    OpenBibleStory,
    PublishRequest,
    LicenseAgreement
)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "website", "phone", "location", "other", "checking_entity"]
    list_display_links = ["name"]
    list_filter = ["checking_entity"]
    search_fields = ["name", "email", "phone", "other"]


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ["con_src", "con_type", "con_dst"]
    list_display_links = ["con_src"]
    list_filter = ["con_type"]
    search_fields = ["con_src", "con_dst"]


class ConnectionTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "mutual"]
    list_display_links = ["name"]
    search_fields = ["name"]


class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "d43username", "email", "phone", "other"]
    list_display_links = ["name"]
    search_fields = ["name", "email", "phone", "other"]


class RecentCommunicationAdmin(admin.ModelAdmin):
    list_display = ["contact", "communication", "created", "created_by"]
    list_display_links = ["contact"]
    list_filter = ["contact", "created", "created_by"]
    search_fields = ["contact", "communication"]


class SourceTextFilter(admin.SimpleListFilter):
    title = "Source Text"
    parameter_name = "language"

    def lookups(self, request, model_admin):
        texts = [
            (str(x.source_text.pk), x.source_text.langcode)
            for x in
            model_admin.queryset(request).filter(source_text__checking_level=3).distinct()
        ]
        if model_admin.queryset(request).filter(source_text__isnull=True).exists():
            texts.append(("NoneSelected", "None"))
        return texts

    def queryset(self, request, queryset):
        print self.value()
        if self.value() == "NoneSelected":
            return queryset.filter(source_text__isnull=True)
        if self.value():
            return queryset.filter(source_text__pk=self.value())
        return queryset.filter(Q(source_text__isnull=True) | Q(source_text__checking_level=3))


class OpenBibleStoryAdmin(reversion.VersionAdmin):
    list_display = ["language", "contact", "date_started", "notes", "publish_date", "version", "checking_level", "source_text", "source_version", "created", "created_by"]
    list_display_links = ["language"]
    list_editable = ["contact", "notes"]
    list_filter = ["contact", "date_started", "checking_level", "publish_date", "version", SourceTextFilter, "source_version"]
    search_fields = ["contact", "notes", "language", "publish_date", "version", "checking_entity", "checking_level", "contributors", "source_text", "source_version", "created_by"]


class LicenseAgreementInline(admin.TabularInline):
    model = LicenseAgreement


class PublishRequestAdmin(admin.ModelAdmin):
    list_display = ["requestor", "resource", "language", "checking_level", "contributors"]
    list_filter = ["checking_level"]
    inlines = [LicenseAgreementInline]


admin.site.register(Contact, ContactAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(ConnectionType, ConnectionTypeAdmin)
admin.site.register(RecentCommunication, RecentCommunicationAdmin)
admin.site.register(OpenBibleStory, OpenBibleStoryAdmin)
admin.site.register(PublishRequest, PublishRequestAdmin)
