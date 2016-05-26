from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _, override

from django_comments.models import CommentAbstractModel
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase, TaggedItemBase


class CommentTag(TagBase):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    @property
    def plain(self):
        return "#" + self.slug

    @property
    def html(self):
        object_url = self.content_object.get_absolute_url() if hasattr(self.content_object, "get_absolute_url") else ""
        return "<a class=\"comment-tag\" href=\"" + object_url + "\">" + self.plain + "</a>"


class TaggedObject(GenericTaggedItemBase):
    tag = models.ForeignKey(CommentTag, related_name="%(app_label)s_%(class)s_items")


class CommentWithTags(CommentAbstractModel):
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
