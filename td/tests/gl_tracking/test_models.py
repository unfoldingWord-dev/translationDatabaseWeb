from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
# from mock import Mock

from td.tracking.models import Language
from td.gl_tracking.models import (
    Phase,
    DocumentCategory,
    Document,
    Progress,
    Partner,
    Method,
    GLDirector,
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


class ProgressTestCase(TestCase):

    def setUp(self):
        phase = Phase.objects.create(number="1")
        doc_cat = DocumentCategory.objects.create(
            name="Test Category",
            phase=phase
        )
        self.doc = Document.objects.create(
            name="Test Document",
            code="td",
            category=doc_cat
        )
        self.language = Language.objects.create(code="tl")

    def test_string_representation(self):
        """
        Progress should be represented by its type's name
        """
        object = Progress.objects.create(language=self.language, type=self.doc)
        self.assertEqual(object.__str__(), "Test Document")

    def test_save_new(self):
        """
        When saving Progress:
           created_at should be set almost immediately
           modified_at should be set almost immediately
           created_at and modified_at should be almost identical
        """
        object = Progress(language=self.language, type=self.doc)
        object.save()
        delta_created = timezone.now() - object.created_at
        delta_modified = timezone.now() - object.modified_at
        delta = object.modified_at - object.created_at
        self.assertAlmostEqual(delta_created.seconds, 0)
        self.assertAlmostEqual(delta_modified.seconds, 0)
        self.assertAlmostEqual(delta.seconds, 0)

    def test_save_modify(self):
        """
        When modifying Progress:
           created_at should stay the same at creation
           modified_at should be changed at modification
           modified_at should be different than created_at
        """
        object = Progress(language=self.language, type=self.doc)
        object.save()
        created1 = object.created_at
        modified1 = object.modified_at
        object.is_online = True
        object.save()
        created2 = object.created_at
        modified2 = object.modified_at
        delta = timezone.now() - object.modified_at
        self.assertEqual(created1, created2)
        self.assertNotEqual(modified1, modified2)
        self.assertAlmostEqual(delta.seconds, 0)


class PartnerTestCase(TestCase):

    def test_string_representation(self):
        """
        Partner should be represented by its name
        """
        name = "Test Partner"
        object = Partner.objects.create(name=name)
        self.assertEqual(object.__str__(), name)


class MethodTestCase(TestCase):

    def test_string_representation(self):
        """
        Method should be represented by its name
        """
        name = "Test Method"
        object = Method.objects.create(name=name)
        self.assertEqual(object.__str__(), name)


class GLDirectorTestCase(TestCase):

    def test_string_representation(self):
        """
        GLDirector should be represented by its username
        """
        name = "Test User"
        user = User.objects.create_user(username=name)
        object = GLDirector.objects.create(user=user)
        self.assertEqual(object.__str__(), name)
