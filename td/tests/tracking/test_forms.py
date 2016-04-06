from mock import Mock
from datetime import date

from django.forms import forms
from django.test import TestCase

from td.tracking.forms import check_end_date, check_text_input


class CheckEndDateTestCase(TestCase):

    def test_no_start_date(self):
        """
        Absence of start_date should raise ValidationError
        """
        mock_cleaned_data = {"end_date": date(2016, 6, 4)}
        with self.assertRaises(forms.ValidationError):
            check_end_date(mock_cleaned_data)

    def test_same_date(self):
        """
        Same end_date and start_date should raise ValidationError
        """
        mock_cleaned_data = {
            "start_date": date(2016, 6, 4),
            "end_date": date(2016, 6, 4)
        }
        with self.assertRaises(forms.ValidationError):
            check_end_date(mock_cleaned_data)

    def test_end_early(self):
        """
        Earlier end_date should raise ValidationError
        """
        mock_cleaned_data = {
            "start_date": date(2016, 6, 4),
            "end_date": date(2016, 6, 3)
        }
        with self.assertRaises(forms.ValidationError):
            check_end_date(mock_cleaned_data)

    def test_end_later(self):
        """
        Later end_date sould return the end_date
        """
        mock_cleaned_data = {
            "start_date": date(2016, 6, 4),
            "end_date": date(2016, 6, 5)
        }
        self.assertEqual(check_end_date(mock_cleaned_data), date(2016, 6, 5))


class CheckTextInputTestCase(TestCase):

    def setUp(self):
        self.form = Mock()

    def test_empty_field(self):
        """
        Empty field should raise ValidationError
        """
        self.form.cleaned_data = {"field": ""}
        with self.assertRaises(forms.ValidationError):
            check_text_input(self.form, "field")

    def test_whitespace(self):
        """
        Whitespaces should be counted as empty and should raise ValidationError
        """
        self.form.cleaned_data = {"field": "   "}
        with self.assertRaises(forms.ValidationError):
            check_text_input(self.form, "field")

    def test_valid_entry(self):
        """
        Valid entry, even with leading and trailing whitespaces, should return said entry
        """
        self.form.cleaned_data = {"field": " some text "}
        self.assertEqual(check_text_input(self.form, "field"), "some text")
