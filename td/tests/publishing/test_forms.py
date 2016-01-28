from django.contrib.auth.models import User
from django.test import TestCase

from td.publishing.models import RecentCommunication, Contact
from td.publishing.forms import RecentComForm, PublishRequestForm, PublishRequestNoAuthForm


class RecentComFormTestCase(TestCase):
    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            first_name="Test",
            last_name="User",
            username="test_user",
        )
        self.user.set_password('test_password')
        self.user.save()
        self.contact, _ = Contact.objects.get_or_create(
            name="Test Contact",
            email="testcontact@example.com",
            d43username="test_user",
            location="Foo, Bar",
        )
        self.recent_com, _ = RecentCommunication.objects.get_or_create(
            communication="Test communication",
            created_by=self.user,
            contact=self.contact,
        )

    def test_empty_valid_form(self):
        form = RecentComForm(
            {},
            self.recent_com,
            user=self.user,
            contact=self.contact
        )
        self.assertTrue(form.is_valid())

    def test_save_valid_form(self):
        form_data = {
            "communication": "New communication message",
        }
        form = RecentComForm(
            form_data,
            self.recent_com,
            user=self.user,
            contact=self.contact
        )
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(
            form.cleaned_data["communication"],
            "New communication message"
        )


class PublishRequestFormNewRequestTestCase(TestCase):

    def test_rejected_fields(self):
        form = PublishRequestNoAuthForm({}, None)
        self.assertFalse('rejected_at' in form.fields)


class PublishRequestFormEditRequestTestCase(TestCase):

    def test_rejected_fields(self):
        form = PublishRequestForm({}, None)
        self.assertTrue('rejected_at' in form.fields)
