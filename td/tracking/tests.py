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


class ModelTestCase(TestCase):

    fixtures = ["td_tracking_seed.json"]

    def test_charter_string_representation(self):
        now = datetime.datetime.now()
        department = Department.objects.get(pk=1)
        language = Language.objects.create(code="wa")
        charter = Charter.objects.create(language=language, start_date=now, end_date=now, lead_dept=department)
        self.assertEqual(str(charter), "wa")

    def test_department_string_representation(self):
        department = Department.objects.create(name="Testing Services")
        self.assertEqual(str(department), "Testing Services")

    def test_hardware_string_representation(self):
        hardware = Hardware.objects.create(name="Test Hardware")
        self.assertEqual(str(hardware), "Test Hardware")

    def test_software_string_representation(self):
        software = Software.objects.create(name="Testing Software")
        self.assertEqual(str(software), "Testing Software")

    def test_translationmethod_string_representation(self):
        translation_methods = TranslationMethod.objects.create(name="Translation Service")
        self.assertEqual(str(translation_methods), "Translation Service")


class ViewsTestCase(TestCase):

    fixtures = ["td_tracking_seed.json"]

    def setUp(self):
        self.credentials = {"username": "testuser", "password": "testpassword"}
        User.objects.create_user(**self.credentials)

    # Home

    def test_home_view_success(self):
        response = self.client.get("/tracking/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "tracking/project_list.html")
        self.assertIn("<h1>Tracking Dashboard</h1>", response.content)

    # New Charter

    def test_new_charter_view_no_login(self):
        response = self.client.get("/tracking/charter/new/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/account/login/?next=/tracking/charter/new/")

    def test_new_charter_view_with_login(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/tracking/charter/new/", **self.credentials)
        self.assertEqual(response.status_code, 200)

    def test_new_charter_view_with_param(self):
        response = self.client.get("/tracking/charter/new/99")
        self.assertEqual(response.status_code, 404)

    def test_new_charter_view_correct_template(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/tracking/charter/new/", **self.credentials)
        self.assertIn("New Translation Project Charter", response.content)

    def test_new_charter_view_default_start_date(self):
        date = datetime.datetime.now()
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/tracking/charter/new/", **self.credentials)
        month_option_string = "<option value=\"" + str(date.month) + "\" selected=\"selected\">"
        day_option_string = "<option value=\"" + str(date.day) + "\" selected=\"selected\">"
        year_option_string = "<option value=\"" + str(date.year) + "\" selected=\"selected\">"
        self.assertIn(month_option_string, response.content)
        self.assertIn(day_option_string, response.content)
        self.assertIn(year_option_string, response.content)

    def test_new_charter_view_default_created_by(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/tracking/charter/new/", **self.credentials)
        created_by_string = "name=\"created_by\" type=\"hidden\" value=\"testuser\""
        self.assertIn(created_by_string, response.content)

    # Update Charter

    def test_charter_upadate_view_no_login(self):
        response = self.client.get("/tracking/charter/update/99/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/account/login/?next=/tracking/charter/update/99/")

    def test_charter_upadate_view_with_login_not_found(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/tracking/charter/update/99/", **self.credentials)
        self.assertEqual(response.status_code, 404)

    def test_charter_upadate_view_no_param(self):
        response = self.client.get("/tracking/charter/update/")
        self.assertEqual(response.status_code, 404)

    def test_charter_update_view_correct_template(self):
        now = datetime.datetime.now()
        department = Department.objects.get(pk=1)
        language = Language.objects.create(code="wa")
        charter = Charter.objects.create(language=language, start_date=now, end_date=now, lead_dept=department)
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/tracking/charter/update/" + str(charter.id) + "/", **self.credentials)
        self.assertIn("Update Translation Project Charter", response.content)

    # Charter Detail

    def test_charter_detail_page(self):

        response = self.client.get("/tracking/charter/detail/99")
        self.assertEqual(response.status_code, 301)

        response = self.client.get("/tracking/charter/detail/")
        self.assertEqual(response.status_code, 404)

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


class UrlsTestCase(TestCase):

    def test_url_reverse(self):
        url = reverse("tracking:project_list")
        self.assertEqual(url, "/tracking/")

        url = reverse("tracking:ajax_ds_charter_list")
        self.assertEqual(url, "/tracking/ajax/charters/")

        url = reverse("tracking:charter_add")
        self.assertEqual(url, "/tracking/charter/new/")

        url = reverse("tracking:charter", args=[999])
        self.assertEqual(url, "/tracking/charter/detail/999/")

        url = reverse("tracking:charter_update", args=[999])
        self.assertEqual(url, "/tracking/charter/update/999/")

        url = reverse("tracking:charter_add_success", kwargs={"obj_type": "charter", "pk": "999"})
        self.assertEqual(url, "/tracking/success/charter/999/")

    def test_url_resolve_home(self):
        """
        URL for tracking home resolves to correct setting
        """

        resolver = resolve("/tracking/")
        self.assertEqual(resolver.url_name, "project_list")
        self.assertEqual(resolver.namespace, "tracking")
        self.assertEqual(resolver.view_name, "tracking:project_list")

    def test_url_resolve_ajax_charters(self):
        """
        URL for ajax charter resolves to correct setting
        """

        resolver = resolve("/tracking/ajax/charters/")
        self.assertEqual(resolver.namespace, "tracking")
        self.assertEqual(resolver.view_name, "tracking:ajax_ds_charter_list")
        self.assertEqual(resolver.url_name, "ajax_ds_charter_list")

    def test_url_resolve_charter_new(self):
        """
        URL for new charter form resolves to correct setting
        """

        resolver = resolve("/tracking/charter/new/")
        self.assertEqual(resolver.namespace, "tracking")
        self.assertEqual(resolver.view_name, "tracking:charter_add")
        self.assertEqual(resolver.url_name, "charter_add")

    def test_url_resolve_charter_add_success(self):
        """
        URL for new charter success resolves to correct setting
        """

        resolver = resolve("/tracking/success/charter/999/")
        self.assertIn("pk", resolver.kwargs)
        self.assertIn("obj_type", resolver.kwargs)
        self.assertEqual(resolver.kwargs["pk"], "999")
        self.assertEqual(resolver.kwargs["obj_type"], "charter")
        self.assertEqual(resolver.namespace, "tracking")
        self.assertEqual(resolver.view_name, "tracking:charter_add_success")
        self.assertEqual(resolver.url_name, "charter_add_success")

    def test_url_resolve_charter_update(self):
        """
        URL for update resolves to correct setting
        """

        resolver = resolve("/tracking/charter/update/999/")
        self.assertIn("pk", resolver.kwargs)
        self.assertEqual(resolver.kwargs["pk"], "999")
        self.assertEqual(resolver.namespace, "tracking")
        self.assertEqual(resolver.view_name, "tracking:charter_update")
        self.assertEqual(resolver.url_name, "charter_update")

    def test_url_resolve_charter_detail(self):
        """
        URL for charter detail resolves to correct setting
        """

        resolver = resolve("/tracking/charter/detail/999/")
        self.assertIn("pk", resolver.kwargs)
        self.assertEqual(resolver.kwargs["pk"], "999")
        self.assertEqual(resolver.namespace, "tracking")
        self.assertEqual(resolver.view_name, "tracking:charter")
        self.assertEqual(resolver.url_name, "charter")


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
