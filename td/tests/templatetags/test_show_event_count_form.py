import types

from django.core.urlresolvers import reverse
from django.test import TestCase

from td.models import WARegion, Country, Language
from td.templatetags.show_event_count_form import show_event_count_form


class ShowEventCountFormTestCase(TestCase):

    def setUp(self):
        self.wa_region, _ = WARegion.objects.get_or_create(name="Middle Earth", slug="me")
        self.country, _ = Country.objects.get_or_create(name="Gondor", code="go")
        self.country.wa_region = self.wa_region
        self.country.save()
        self.language, _ = Language.objects.get_or_create(name="Valarin", code="val")
        self.language.country = self.country
        self.language.save()

    def test_context_returned(self):
        context = show_event_count_form({})
        self.assertIsInstance(context, types.DictionaryType)
        self.assertIn("mode", context)
        self.assertIn("selected_option", context)
        self.assertIn("selected_fy", context)
        self.assertIn("form_action", context)
        self.assertIn("options", context)
        self.assertIn("fiscal_years", context)
        self.assertIn("container", context)

    def test_dashboard_mode_implicit(self):
        context = show_event_count_form({})
        self.assertEqual(context["mode"], "dashboard")
        self.assertListEqual(context["options"], [("me", "Middle Earth")])
        self.assertIsNone(context["selected_option"])

    def test_region_mode_implicit(self):
        context = show_event_count_form({"wa_region": self.wa_region})
        self.assertEqual(context["mode"], "region")
        self.assertListEqual(context["options"], [("me", "Middle Earth")])
        self.assertEqual(context["selected_option"], "me")

    def test_country_mode_implicit(self):
        context = show_event_count_form({"country": self.country})
        self.assertEqual(context["mode"], "country")
        self.assertListEqual(context["options"], [("go", "Gondor")])
        self.assertEqual(context["selected_option"], "go")

    def test_language_mode_implicit(self):
        context = show_event_count_form({"language": self.language})
        self.assertEqual(context["mode"], "language")
        self.assertListEqual(context["options"], [("val", "Valarin")])
        self.assertEqual(context["selected_option"], "val")

    def test_dashboard_mode_explicit(self):
        context = show_event_count_form({}, mode="dashboard")
        self.assertEqual(context["mode"], "dashboard")
        self.assertListEqual(context["options"], [("me", "Middle Earth")])
        self.assertIsNone(context["selected_option"])

    def test_region_mode_explicit(self):
        context = show_event_count_form({}, mode="region")
        self.assertEqual(context["mode"], "region")
        self.assertListEqual(context["options"], [])
        self.assertIsNone(context["selected_option"])

    def test_country_mode_explicit(self):
        context = show_event_count_form({}, mode="country")
        self.assertEqual(context["mode"], "country")
        self.assertListEqual(context["options"], [])
        self.assertIsNone(context["selected_option"])

    def text_language_mode_explicit(self):
        context = show_event_count_form({}, mode="language")
        self.assertEqual(context["mode"], "language")
        self.assertListEqual(context["options"], [])
        self.assertIsNone(context["selected_option"])

    def test_selected_option_implicit(self):
        context = show_event_count_form({}, mode="dashboard", selected_option="")
        self.assertEqual(context["mode"], "dashboard")
        self.assertEqual(context["selected_option"], "")
        context = show_event_count_form({}, mode="dashboard", selected_option="me")
        self.assertEqual(context["mode"], "dashboard")
        self.assertEqual(context["selected_option"], "me")
        context = show_event_count_form({}, mode="region", selected_option="")
        self.assertEqual(context["mode"], "region")
        self.assertEqual(context["selected_option"], "")
        context = show_event_count_form({}, mode="region", selected_option="go")
        self.assertEqual(context["mode"], "region")
        self.assertEqual(context["selected_option"], "go")
        context = show_event_count_form({}, mode="country", selected_option="")
        self.assertEqual(context["mode"], "country")
        self.assertEqual(context["selected_option"], "")
        context = show_event_count_form({}, mode="country", selected_option="val")
        self.assertEqual(context["mode"], "country")
        self.assertEqual(context["selected_option"], "val")
        context = show_event_count_form({}, mode="language", selected_option="")
        self.assertEqual(context["mode"], "language")
        self.assertEqual(context["selected_option"], "")
        context = show_event_count_form({}, mode="language", selected_option="val")
        self.assertEqual(context["mode"], "language")
        self.assertEqual(context["selected_option"], "val")

    def test_selected_fy_implicit(self):
        context = show_event_count_form({})
        self.assertEqual(context["selected_fy"], "0")

    def test_selected_fy_explicit(self):
        context = show_event_count_form({}, selected_fy="0")
        self.assertEqual(context["selected_fy"], "0")
        context = show_event_count_form({}, selected_fy="1")
        self.assertEqual(context["selected_fy"], "1")
        context = show_event_count_form({}, selected_fy="-1")
        self.assertEqual(context["selected_fy"], "-1")

    def test_fiscal_years(self):
        context = show_event_count_form({})
        self.assertEqual(len(context["fiscal_years"]), 6)
        for entry in context["fiscal_years"]:
            self.assertIsInstance(entry, types.TupleType)
            self.assertEqual(len(entry), 2)
            self.assertIsInstance(entry[1], types.StringType)

    def test_container_implicit(self):
        context = show_event_count_form({})
        self.assertEqual(context["container"], "")

    def test_container_explicit(self):
        context = show_event_count_form({}, container=".container")
        self.assertEqual(context["container"], ".container")

    def test_form_action_implicit(self):
        context = show_event_count_form({})
        self.assertEqual(context["form_action"], reverse("tracking:event_count"))

    def test_form_action_explicit(self):
        url = "/some/url/"
        context = show_event_count_form({}, form_action=url)
        self.assertEqual(context["form_action"], url)

    def test_form_action_with_container(self):
        url = "/some/url/"
        context = show_event_count_form({}, form_action=url, container=".container")
        self.assertEqual(context["form_action"], "")
        self.assertEqual(context["container"], ".container")
