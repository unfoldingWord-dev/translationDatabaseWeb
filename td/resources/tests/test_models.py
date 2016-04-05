from django.test import TestCase
from ..models import Resource, Media, Title, Publisher, Questionnaire
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
        super(ResourceTestCase, cls).setUpClass()
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


class QuestionnaireTestCase(TestCase):
    def setUp(self):
        self.questions = [
            {
                "id": 0,
                "text": "What do you call your language?",
                "help": "Test help text",
                "required": True,
                "input_type": "string",
                "sort": 1,
                "depends_on": None
            },
            {
                "id": 1,
                "text": "Second Question",
                "help": "Test help text",
                "required": True,
                "input_type": "string",
                "sort": 2,
                "depends_on": 0
            },
            {
                "id": 2,
                "text": "Third Question",
                "help": "Test help text",
                "required": True,
                "input_type": "string",
                "sort": 3,
                "depends_on": None
            }
        ]
        self.obj = Questionnaire.objects.create(pk=999, questions=self.questions)

    def test_string_representation(self):
        """ Questionnaire should be displayed as its pk """
        self.assertEquals(str(self.obj), "999")

    def test_grouped_questions_property(self):
        """ Questionnaire.grouped_question should return a nested array of questions grouped by 'depends_on' """
        expected = [
            [self.questions[0], self.questions[1]],
            [self.questions[2]]
        ]
        self.assertListEqual(self.obj.grouped_questions, expected)
