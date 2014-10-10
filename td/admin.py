from django.contrib import admin

from .models import AdditionalLanguage


admin.site.register(
    AdditionalLanguage,
    list_display=[
        "ietf_tag",
        "common_name",
        "two_letter",
        "three_letter",
        "native_name",
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
