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
        cls.title.save()
        cls.media = Media(name="Media Title", slug="test-media")
        cls.media.save()
        cls.language = Language(code="ztest", name="Z Language")
        cls.language.save()

    def test_string_representation(self):
        resource = Resource(language=self.language, title=self.title)
        resource.save()
        resource.medias.add(self.media)
        resource.save()
        self.assertEquals(str(resource), "Test Title in Z Language")
