from django.test import TestCase
from ..models import Resource, Media, Title, Publisher
from td.models import Language


class MediaTestCase(TestCase):
    def test_string_representation(self):
        media = Media(name="Test Media", slug="test-media")
        self.assertEquals(str(media), "Test Media")


class TitleTestCase(TestCase):
    def test_string_representation(self):
        title = Title(name="Test Title", slug="test-title")
        self.assertEquals(str(title), "Test Title")


class PublisherTestCase(TestCase):
    def test_string_representation(self):
        publisher = Publisher(name="Test Publisher")
        self.assertEquals(str(publisher), "Test Publisher")


class ResourceTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.publisher = Publisher(name="Test Publisher 1")
        cls.publisher.save()
        cls.publisher2 = Publisher(name="Test Publisher 2")
        cls.publisher2.save()
        cls.title = Title(name="Test Title", slug="test-title")
        cls.title.publisher = cls.publisher
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
        self.assertEquals(str(resource.the_publisher()), "Test Publisher 1")
        resource.publisher = self.publisher2
        resource.save()
        self.assertEquals(str(resource.the_publisher()), "Test Publisher 2")
