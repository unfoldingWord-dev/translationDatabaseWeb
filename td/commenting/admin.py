from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import get_model
from .models import CommentWithTags
from django_comments.admin import CommentsAdmin


class CommentWithTagsAdmin(CommentsAdmin):
    fieldsets = (
        (None, {"fields": ("content_type", "object_pk", "site")}),
        (_("Content"), {"fields": ("user", "user_name", "user_email", "user_url", "comment", "tags")}),
        (_("Metadata"), {"fields": ("submit_date", "ip_address", "is_public", "is_removed")}),
    )

if get_model() is CommentWithTags:
    admin.site.register(CommentWithTags, CommentWithTagsAdmin)
