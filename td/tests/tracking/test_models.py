from django.test import TestCase
from django.utils import timezone

from td.tracking.models import (
    Charter,
    Event,
    Department,
    TranslationMethod,
    Software,
    Hardware,
    Material,
    Translator,
    Facilitator,
    Output,
    Publication,
)
from td.models import Language


class CharterTestCase(TestCase):

    def setUp(self):
        language = Language.objects.create(
            id=9999,
            code="ts",
            name="Test Language",
        )
        department = Department.objects.create(
            name="Test Department",
        )
        self.model = Charter.objects.create(
            language=language,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
        )

    def test_unicode(self):
        """
        Charter should be represented by the code of its language
        """
        self.assertEqual(self.model.__unicode__(), "ts")

    def test_lang_id(self):
        """
        Charter.lang_id should return the ID of its language
        """
        self.assertEqual(self.model.lang_id, 9999)

    def test_lang_data(self):
        """
        lang_data() should return desired dict
        """
        data = self.model.lang_data()
        self.assertEqual(data[0]["pk"], 9999)
        self.assertEqual(data[0]["lc"], "ts")
        self.assertEqual(data[0]["ln"], "Test Language")
        self.assertEqual(data[0]["cc"], [""])
        self.assertEqual(data[0]["lr"], "")


class EventTestCase(TestCase):

    def setUp(self):
        language, _ = Language.objects.get_or_create(
            id=9999,
            code="ts",
            name="Test Language",
        )
        department, _ = Department.objects.get_or_create(
            name="Test Department",
        )
        charter, _ = Charter.objects.get_or_create(
            language=language,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
        )
        self.model, _ = Event.objects.get_or_create(
            id=9999,
            charter=charter,
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            lead_dept=department,
            location="Test Location",
        )

    def test_unicode(self):
        """
        Event should be represented by its ID
        """
        self.assertEqual(self.model.__unicode__(), "9999")


class TranslationMethodTestCase(TestCase):

    def setUp(self):
        self.model, _ = TranslationMethod.objects.get_or_create(
            name="Test Translation Method",
        )

    def test_unicode(self):
        """
        TranslationMethod should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Translation Method")


class SoftwareTestCase(TestCase):

    def setUp(self):
        self.model, _ = Software.objects.get_or_create(
            name="Test Software",
        )

    def test_unicode(self):
        """
        Software should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Software")


class HardwareTestCase(TestCase):

    def setUp(self):
        self.model, _ = Hardware.objects.get_or_create(
            name="Test Hardware",
        )

    def test_unicode(self):
        """
        Hardware should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Hardware")


class MaterialTestCase(TestCase):

    def setUp(self):
        self.model, _ = Material.objects.get_or_create(
            name="Test Material",
        )

    def test_unicode(self):
        """
        Material should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Material")


class TranslatorTestCase(TestCase):

    def setUp(self):
        self.model, _ = Translator.objects.get_or_create(
            name="Test Translator",
        )

    def test_unicode(self):
        """
        Translator should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Translator")


class FacilitatorTestCase(TestCase):

    def setUp(self):
        self.model, _ = Facilitator.objects.get_or_create(
            name="Test Facilitator",
        )

    def test_unicode(self):
        """
        Facilitator should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Facilitator")


class DepartmentTestCase(TestCase):

    def setUp(self):
        self.model, _ = Department.objects.get_or_create(
            name="Test Department",
        )

    def test_unicode(self):
        """
        Department should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Department")


class OutputTestCase(TestCase):

    def setUp(self):
        self.model, _ = Output.objects.get_or_create(
            name="Test Output",
        )

    def test_unicode(self):
        """
        Output should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Output")


class PublicationTestCase(TestCase):

    def setUp(self):
        self.model, _ = Publication.objects.get_or_create(
            name="Test Publication",
        )

    def test_unicode(self):
        """
        Publication should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Publication")
