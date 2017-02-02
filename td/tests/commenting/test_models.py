from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType

from ..models import NoSignalTestCase
from ...models import Language
from ...commenting.models import CommentTag


class CommentTagTestCase(NoSignalTestCase):

    def setUp(self):
        super(CommentTagTestCase, self).setUp()
        self.language = Language.objects.create(name="Test Language", code="tlang")
        content_type = ContentType.objects.get_for_model(self.language)
        self.comment = CommentTag.objects.create(name=self.language.tag_slug, slug=self.language.tag_slug,
                                                 object_id=self.language.id, content_type=content_type)

    def tearDown(self):
        super(CommentTagTestCase, self).tearDown()

    def test_plain(self):
        """ 'plain' property must return object's tag_slug prepended with '#' """
        self.assertEqual(self.comment.plain, "#" + self.language.tag_slug)

    def test_html_with_absolute_url(self):
        """ 'html' property must contain the object's absolute_url """
        language_url = self.language.get_absolute_url()
        self.assertIn(language_url, self.comment.html)
