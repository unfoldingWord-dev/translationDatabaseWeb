from django.contrib import admin

from .models import (
    EthnologueCountryCode,
    EthnologueLanguageCode,
    EthnologueLanguageIndex,
    SIL_ISO_639_3,
    WikipediaISOLanguage
)


admin.site.register(
    EthnologueCountryCode,
    list_display=[
        "code", "name", "area", "date_imported"
    ],
    list_filter=[
        "area"
    ],
    search_fields=[
        "code", "name", "area"
    ]
)


admin.site.register(
    EthnologueLanguageCode,
    list_display=[
        "code", "country_code", "status", "name", "date_imported"
    ],
    list_filter=[
        "country_code", "status"
    ],
    search_fields=[
        "code", "name"
    ]
)


admin.site.register(
    EthnologueLanguageIndex,
    list_display=[
        "language_code", "country_code", "name_type", "name", "date_imported"
    ],
    list_filter=[
        "name_type", "country_code"
    ],
    search_fields=[
        "language_code", "name"
    ]
)


admin.site.register(
    WikipediaISOLanguage,
    list_display=[
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
    ],
    list_filter=[
        "language_family"
    ],
    search_fields=[
        "language_name",
        "native_name",
        "notes"
    ]
)


admin.site.register(
    SIL_ISO_639_3,
    list_display=[
        "code",
        "part_2b",
        "part_2t",
        "part_1",
        "scope",
        "language_type",
        "ref_name",
        "comment",
        "date_imported",
    ],
    list_filter=[
        "scope",
        "language_type"
    ],
    search_fields=[
        "comment",
        "ref_name"
    ]
)
