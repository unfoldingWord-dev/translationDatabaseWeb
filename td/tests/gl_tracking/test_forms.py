from django.test import TestCase
from datetime import date

from td.gl_tracking.forms import PartnerForm


class PartnerFormTestCase(TestCase):
    def test_name_form(self):
        form = PartnerForm(
            {"name": "Partner Name"},
        )
        self.assertEqual(form.is_valid(), True)

    def test_blank_form(self):
        """
        Test a blank form
        """
        form = PartnerForm()
        self.assertEqual(form.is_valid(), False)

    def test_date_failure(self):
        """
        Test to make sure validation fails if the partner_start is after the partner_end
        """
        form = PartnerForm(
            {"name": "Partner Name",
             "partner_start": date(2016, 1, 2),
             "partner_end": date(2016, 1, 1),
             }
        )
        self.assertEqual(form.has_error("partner_end"), True)

    def test_date_valid(self):
        """
        Test that the validation succeeds with the partner_start being after the partner_end
        """
        form = PartnerForm(
            {"name": "Partner Name",
             "partner_start": date(2016, 1, 1),
             "partner_end": date(2016, 1, 2),
             }
        )
        self.assertEqual(form.has_error("partner_end"), False)

    def test_date_only_end(self):
        """
        Test that the validation succeeds with just the partner end
        """
        test_date = date(2016, 1, 2)
        form = PartnerForm(
            {"name": "Partner Name",
             "partner_end": test_date,
             }
        )
        self.assertEqual(form.has_error("partner_end"), False)
        self.assertEqual(form.cleaned_data["partner_end"], test_date)
