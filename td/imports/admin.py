from django.contrib import admin

from .models import WikipediaISOLanguage


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
    ]
)
