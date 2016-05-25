from __future__ import unicode_literals

from django_comments.models import CommentAbstractModel
from taggit.managers import TaggableManager


class CommentWithTags(CommentAbstractModel):
    tags = TaggableManager(blank=True)
