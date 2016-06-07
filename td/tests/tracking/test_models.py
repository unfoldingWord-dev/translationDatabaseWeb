import types

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from td.commenting.models import CommentWithTags
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
from td.utils import ordinal


class CharterTestCase(TestCase):

    def setUp(self):
        language = Language.objects.create(id=9999, code="ts", name="Test Language")
        self.department = Department.objects.create(name="Test Department")
        self.model = Charter.objects.create(language=language, start_date=timezone.now().date(),
                                            end_date=timezone.now().date(), lead_dept=self.department)

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

    def test_get_absolute_url(self):
        expected_result = reverse("language_detail", kwargs={"pk": self.model.language_id})
        self.assertEqual(self.model.get_absolute_url(), expected_result)

    def test_tag_display(self):
        expected_result = "%s-Project" % self.model.language.tag_display
        self.assertEqual(self.model.tag_display, expected_result)

    def test_tag_tip(self):
        expected_result = self.model.language.tag_tip
        self.assertEqual(self.model.tag_tip, expected_result)

    def test_all_events_comments_wo_events(self):
        self.assertListEqual(self.model.all_events_comments, [])

    def test_all_events_comments_w_events_wo_comments(self):
        Event.objects.get_or_create(charter=self.model, start_date=timezone.now().date(),
                                    end_date=timezone.now().date(), lead_dept=self.department, location="Test Location")
        self.assertListEqual(self.model.all_events_comments, [])

    def test_all_events_comments_w_events_w_comments(self):
        start_date = timezone.now().date()
        end_date = timezone.now().date()
        # WHY: If the "id" are not specified, self.model.event_set.all() only shows 1 event in the charter.
        event_1, _ = Event.objects.get_or_create(id=999, charter=self.model, start_date=start_date, end_date=end_date,
                                                 lead_dept=self.department, location="wrong location")
        event_2, _ = Event.objects.get_or_create(id=998, charter=self.model, start_date=start_date, end_date=end_date,
                                                 lead_dept=self.department, location="correct location")

        content_type = ContentType.objects.get_for_model(event_2)
        object_id = event_2.id
        comment_1, _ = CommentWithTags.objects.get_or_create(comment="first comment for event 2",
                                                             content_type=content_type, object_pk=object_id, site_id=1)
        comment_2, _ = CommentWithTags.objects.get_or_create(comment="second comment for event 2",
                                                             content_type=content_type, object_pk=object_id, site_id=1)

        result = self.model.all_events_comments
        self.assertIsInstance(result, types.ListType)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], types.DictionaryType)
        self.assertIn("number", result[0])
        self.assertIn("location", result[0])
        self.assertIn("start_date", result[0])
        self.assertIn("end_date", result[0])
        self.assertIn("comments_and_mentions", result[0])
        self.assertEqual(result[0].get("number"), event_2.number)
        self.assertEqual(result[0].get("location"), event_2.location)
        self.assertEqual(result[0].get("start_date"), event_2.start_date)
        self.assertEqual(result[0].get("end_date"), event_2.end_date)
        self.assertEqual(result[0].get("comments_and_mentions"), event_2.comments_and_mentions)


class EventTestCase(TestCase):

    def setUp(self):
        language, _ = Language.objects.get_or_create(id=9999, code="ts", name="Test Language")
        department, _ = Department.objects.get_or_create(name="Test Department")
        charter, _ = Charter.objects.get_or_create(language=language, start_date=timezone.now().date(),
                                                   end_date=timezone.now().date(), lead_dept=department)
        self.model, _ = Event.objects.get_or_create(id=9999, charter=charter, start_date=timezone.now().date(),
                                                    end_date=timezone.now().date(), lead_dept=department,
                                                    location="Test Location", number=1)

    def test_unicode(self):
        """
        Event should be represented by its ID
        """
        self.assertEqual(self.model.__unicode__(), "9999")

    def test_get_absolute_url(self):
        expected_result = reverse("tracking:event_detail", kwargs={"pk": self.model.pk})
        self.assertEqual(self.model.get_absolute_url(), expected_result)

    def test_tag_display(self):
        expected_result = "%s-Project-Event %d" % (self.model.charter.language.tag_display, self.model.number)
        self.assertEqual(self.model.tag_display, expected_result)

    def test_tag_tip(self):
        expected_result = "The %s event of %s project" % (ordinal(self.model.number), self.model.charter.language.tag_display)
        self.assertEqual(self.model.tag_tip, expected_result)


class TranslationMethodTestCase(TestCase):

    def setUp(self):
        self.model, _ = TranslationMethod.objects.get_or_create(name="Test Translation Method")

    def test_unicode(self):
        """
        TranslationMethod should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Translation Method")


class SoftwareTestCase(TestCase):

    def setUp(self):
        self.model, _ = Software.objects.get_or_create(name="Test Software")

    def test_unicode(self):
        """
        Software should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Software")


class HardwareTestCase(TestCase):

    def setUp(self):
        self.model, _ = Hardware.objects.get_or_create(name="Test Hardware")

    def test_unicode(self):
        """
        Hardware should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Hardware")


class MaterialTestCase(TestCase):

    def setUp(self):
        self.model, _ = Material.objects.get_or_create(name="Test Material")

    def test_unicode(self):
        """
        Material should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Material")


class TranslatorTestCase(TestCase):

    def setUp(self):
        self.model, _ = Translator.objects.get_or_create(name="Test Translator")

    def test_unicode(self):
        """
        Translator should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Translator")


class FacilitatorTestCase(TestCase):

    def setUp(self):
        self.model, _ = Facilitator.objects.get_or_create(name="Test Facilitator")

    def test_unicode(self):
        """
        Facilitator should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Facilitator")


class DepartmentTestCase(TestCase):

    def setUp(self):
        self.model, _ = Department.objects.get_or_create(name="Test Department")

    def test_unicode(self):
        """
        Department should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Department")


class OutputTestCase(TestCase):

    def setUp(self):
        self.model, _ = Output.objects.get_or_create(name="Test Output")

    def test_unicode(self):
        """
        Output should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Output")


class PublicationTestCase(TestCase):

    def setUp(self):
        self.model, _ = Publication.objects.get_or_create(name="Test Publication")

    def test_unicode(self):
        """
        Publication should be represented by its name
        """
        self.assertEqual(self.model.__unicode__(), "Test Publication")
