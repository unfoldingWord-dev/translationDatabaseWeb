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


admin.site.register(
    Network,
    list_display=["name"]
)

admin.site.register(
    BibleContent,
    list_display=["name"]
)

admin.site.register(
    Country,
    list_display=["code", "name", "area", "population"]
)

admin.site.register(
    Language,
    list_display=["code", "name", "gateway_language", "native_speakers"]
)

admin.site.register(
    Translator,
    list_display=["name", "email", "d43username", "location", "phone", "relationship", "other"]
)

admin.site.register(
    Organization,
    list_display=["name", "email", "d43username", "location", "phone"]
)

admin.site.register(
    WorkInProgress,
    list_display=["kind", "language", "bible_content", "paradigm", "anticipated_completion_date"]
)

admin.site.register(
    Scripture,
    list_display=["kind", "language", "bible_content", "year", "publisher"]
)

admin.site.register(
    TranslationNeed,
    list_display=["language", "text_gaps", "text_updates", "other_gaps", "other_updates"]
)

admin.site.register(
    Resource,
    list_display=["language", "name", "copyright", "copyright_holder", "license"]
)
