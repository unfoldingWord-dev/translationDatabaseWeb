from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from taggit.admin import TagAdmin
from taggit.models import Tag

from . import get_model
from .models import CommentWithTags, TaggedObject, CommentTag
from django_comments.admin import CommentsAdmin


class TaggedObjectInline(admin.StackedInline):
    model = TaggedObject


class CommentTagAdmin(TagAdmin):
    inlines = [TaggedObjectInline]
    list_display = ["name", "slug", "content_type", "object_id"]
    search_fields = ["name", "slug", "content_type"]


class CommentWithTagsAdmin(CommentsAdmin):
    fieldsets = (
        (None, {"fields": ("content_type", "object_pk", "site")}),
        (_("Content"), {"fields": ("user", "user_name", "user_email", "user_url", "comment", "tags")}),
        (_("Metadata"), {"fields": ("submit_date", "ip_address", "is_public", "is_removed")}),
    )

if get_model() is CommentWithTags:
    admin.site.register(CommentWithTags, CommentWithTagsAdmin)
    admin.site.unregister(Tag)
    admin.site.register(CommentTag, CommentTagAdmin)
