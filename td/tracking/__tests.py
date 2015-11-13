import datetime

from django import forms
from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget

from td.tracking.models import (
    Charter,
    Country,
    Language,
    Department,
    Hardware,
    Software,
    TranslationMethod,
)
from td.tracking.forms import (
    CharterForm,
)


class ViewsTestCase(TestCase):

    # Home

    def test_home_view_no_login(self):
        response = self.client.get("/tracking/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/account/login/?next=/tracking/")

    # New Charter

    def test_new_charter_view_no_login(self):
        response = self.client.get("/tracking/charter/new/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/account/login/?next=/tracking/charter/new/")

    # Update Charter

    def test_charter_upadate_view_no_login(self):
        response = self.client.get("/tracking/charter/update/99/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/account/login/?next=/tracking/charter/update/99/")

    # Success

    def test_success_with_no_login(self):

        response = self.client.get("/tracking/success/charter/99/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/account/login/?next=/tracking/success/charter/99/")

    def test_success_with_login_no_referer(self):

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/tracking/success/charter/99/", **self.credentials)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/tracking/")

    def test_success_with_login_wrong_referer(self):

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/tracking/success/charter/99/", username="testuser", password="testpassword", HTTP_REFERER="http://www.google.com")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/tracking/")

    def test_success_with_login_correct_referer(self):

        now = datetime.datetime.now()
        department = Department.objects.get(pk=1)
        language = Language.objects.create(code="wa")
        charter = Charter.objects.create(language=language, start_date=now, end_date=now, lead_dept=department)
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/tracking/success/charter/" + str(charter.id) + "/", username="testuser", password="testpassword", HTTP_REFERER="http://td.unfoldingword.org/tracking/charter/new/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["link_id"] == str(charter.id))
        self.assertTrue(response.context["status"] == "Success")
        self.assertIn("has been successfully added", response.context["message"])

    # test_success_with_login_correct_referer_wrong_type(self):


class CharterFormTestCase(TestCase):

    def setUp(self):

        self.language = Language(code="py")
        self.language.save()
        self.country = Country(code="uw", name="Unfolding Word")
        self.country.save()
        self.department = Department(name="translationDatabase")
        self.department.save()

    def test_charter_form_incomplete(self):
        """
        Incomplete charter form fails validation
        """

        data = {}
        charter_form = CharterForm(data=data)
        result = charter_form.is_valid()
        self.assertFalse(result)

    def test_charter_form_end_date(self):
        """
        End_date must be later than start_date
        """

        data = {
            "language": 1,
            "countries": 1,
            "start_date_month": "1",
            "start_date_day": "1",
            "start_date_year": "2015",
            "end_date_month": "1",
            "end_date_day": "1",
            "end_date_year": "2015",
            "number": "12345",
            "lead_dept": 1,
            "contact_person": "Vicky Leong",
            "created_by": "Vicky Leong"
        }
        charter_form = CharterForm(data=data)
        result = charter_form.is_valid()
        self.assertFalse(result)

    def test_charter_form_contact_person(self):
        """
        Spaces should be treated as empty string for contact_person
        """

        data = {
            "language": 1,
            "countries": 1,
            "start_date_month": "1",
            "start_date_day": "1",
            "start_date_year": "2015",
            "end_date_month": "2",
            "end_date_day": "2",
            "end_date_year": "2016",
            "number": "12345",
            "lead_dept": 1,
            "contact_person": "   ",
            "created_by": "Vicky Leong"
        }
        charter_form = CharterForm(data=data)
        result = charter_form.is_valid()
        self.assertFalse(result)

    def test_charter_form_complete(self):
        """
        Complete charter form passess validation
        """

        data = {
            "language": self.language.id,
            "countries": [self.country.id],
            "start_date_month": "1",
            "start_date_day": "1",
            "start_date_year": "2015",
            "end_date_month": "2",
            "end_date_day": "2",
            "end_date_year": "2016",
            "number": "12345",
            "lead_dept": 1,
            "contact_person": "Vicky Leong",
            "created_by": "Vicky Leong"
        }
        charter_form = CharterForm(data=data)
        result = charter_form.is_valid()
        self.assertTrue(result)

    def test_charter_form_excluded_fields(self):
        """
        Created_at should not be in the form
        """

        charter_form = CharterForm()
        self.assertNotIn("created_at", charter_form.fields)

    def test_charter_form_date_widgets(self):
        """
        Start_date and end_date must use appropriate widgets
        """

        cf = CharterForm()
        self.assertIsInstance(cf.fields["start_date"].widget, SelectDateWidget)
        self.assertIsInstance(cf.fields["end_date"].widget, SelectDateWidget)
        self.assertEqual(cf.fields["start_date"].widget.attrs["class"], "date-input")
        self.assertEqual(cf.fields["end_date"].widget.attrs["class"], "date-input")

    def test_charter_form_language_widget(self):
        """
        Language must use appropriate widget
        """

        cf = CharterForm()
        language = cf.fields["language"]
        self.assertIsInstance(language.widget, forms.TextInput)
        self.assertEqual(language.widget.attrs["class"], "language-selector")
        self.assertEqual(language.widget.attrs["data-source-url"], reverse("names_autocomplete"))
        self.assertTrue(language.required)
