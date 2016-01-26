from django.test import TestCase
# from django.utils import timezone

from td.gl_tracking.models import (
    Phase,
    DocumentCategory,
    Document,
)
# from td.models import Language


class PhaseTestCase(TestCase):

    def test_string_representation_no_name(self):
        """
        Phase should be represented by 'BT Phase' + its number if it's not
           created with a name
        """
        object1 = Phase.objects.create(number="1")
        self.assertEqual(object1.__str__(), "BT Phase 1")

    def test_string_representation_with_name(self):
        """
        Phase should be represented by its name if it's created with one
        """
        name = "Test Phase"
        object1 = Phase.objects.create(number="1", name=name)
        self.assertEqual(object1.__str__(), name)


class DocumentCategoryTestCase(TestCase):

    def test_string_representation(self):
        """
        DocumentCategory should be represented by its name
        """
        phase = Phase.objects.create(number="1")
        object = DocumentCategory.objects.create(
            name="Test Category",
            phase=phase
        )
        self.assertEqual(object.__str__(), "Test Category")


class DocumentTestCase(TestCase):

    def test_string_representation(self):
        """
        Document should be represented by its name
        """
        phase = Phase.objects.create(number="1")
        doc_cat = DocumentCategory.objects.create(
            name="Test Category",
            phase=phase
        )
        object = Document.objects.create(
            name="Test Document",
            code="td",
            category=doc_cat
        )
        self.assertEqual(object.__str__(), "Test Document")
