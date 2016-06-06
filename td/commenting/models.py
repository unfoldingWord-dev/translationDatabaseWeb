from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from django_comments.models import CommentAbstractModel
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase


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
        return "<a class=\"comment-tag\" href=\"%s\" title=\"%s\">%s</a>" %\
               (object_url, self.content_object.tag_tip, self.content_object.tag_display)


class TaggedObject(GenericTaggedItemBase):
    tag = models.ForeignKey(CommentTag, related_name="%(app_label)s_%(class)s_items")


class CommentWithTags(CommentAbstractModel):
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")


class CommentableModel(models.Model):

    @property
    def tag_slug(self):
        return self.code.lower()

    @property
    def tag_display(self):
        return self.name

    @property
    def tag_tip(self):
        return self.code

    @property
    def hashtag(self):
        return "".join(["#", self.tag_slug])

    @property
    def ctype(self):
        return ContentType.objects.get_for_model(self)

    @property
    def comments(self):
        return list(CommentWithTags.objects.filter(content_type=self.ctype, object_pk=self.pk).select_related("user")
                    .values("comment", "user_name", "submit_date"))

    @property
    def mentions(self):
        qs = list(CommentWithTags.objects.filter(tags__slug__in=[self.tag_slug]).distinct().select_related("user"))
        return [{
            "comment": comment.comment,
            "user_name": comment.user_name,
            "submit_date": comment.submit_date,
            "source": mark_safe("<span class=\"mention-source\"> - mentioned in <a class=\"mention-source-link\"href=\""
                                "%s\">%s</a></span>"
                                % (comment.content_object.get_absolute_url(), comment.content_object.tag_display))
        } for comment in qs]

    @property
    def comments_and_mentions(self):
        return [dict(x) for x in set(tuple(z.items()) for z in self.comments + self.mentions)]

    class Meta:
        abstract = True
