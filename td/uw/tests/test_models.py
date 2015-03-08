from django.test import TestCase
from ..models import Resource, Media, Title, Language


class MediaTestCase(TestCase):
    def test_string_representation(self):
        media = Media(name="Test Media", slug="test-media")
        self.assertEquals(str(media), "Test Media")


class TitleTestCase(TestCase):
    def test_string_representation(self):
        title = Title(name="Test Title", slug="test-title")
        self.assertEquals(str(title), "Test Title")


class ResourceTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.title = Title(name="Test Title", slug="test-title")
        cls.media = Media(name="Media Title", slug="test-media")
        cls.language = Language(code="ztest", name="Z Language")

    def test_string_representation(self):
        resource = Resource(language=self.language, media=self.media, title=self.title)
        self.assertEquals(str(resource), "Test Title in Z Language")
