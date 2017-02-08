from __future__ import absolute_import

from django import forms
from django.test import TestCase

from ..fields import BSDateField, LanguageCharField


class BSDateFieldTestCase(TestCase):

    def setUp(self):
        self.field = BSDateField()

    def test_description(self):
        """ Must have description """
        self.assertGreater(len(self.field.description), 0)

    def test_is_date_input(self):
        """ Widget must be DateInput """
        self.assertIsInstance(self.field.widget, forms.DateInput)

    def test_init_without_input_formats(self):
        """ If input_formats is not passed, it must be initialized with defaults """
        self.assertGreater(len(self.field.input_formats), 0)


class LanguageCharFieldTestCase(TestCase):

    def setUp(self):
        self.field = LanguageCharField()

    def test_description(self):
        """ Must have description """
        self.assertGreater(len(self.field.description), 0)

    def test_is_text_input(self):
        """ Widget must be TextInput """
        self.assertIsInstance(self.field.widget, forms.TextInput)
