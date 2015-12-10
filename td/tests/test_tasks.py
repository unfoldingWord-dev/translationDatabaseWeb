# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from td.tasks import _get_anglicized_language_name


class GetAnglicizedLanguageNameTestCase(TestCase):

    def test_found_in_anglicized_name(self):
        row = ("hi", u"(Hausa) هَوُسَ", "Hausa", "NG", None, 1, None, 1, None, 1, "hau")
        value = _get_anglicized_language_name(row)
        self.assertEqual(value, row[2])

    def test_found_in_nn1name(self):
        row = ("hi", u"(Hausa) هَوُسَ", "", "NG", "Hausa", 1, None, 1, None, 1, "hau")
        value = _get_anglicized_language_name(row)
        self.assertEqual(value, row[4])

    def test_found_in_nn2name(self):
        row = ("hi", u"(Hausa) هَوُسَ", "", "NG", None, 1, "Hausa", 1, None, 1, "hau")
        value = _get_anglicized_language_name(row)
        self.assertEqual(value, row[6])

    def test_found_in_xname(self):
        row = ("hi", u"(Hausa) هَوُسَ", "", "NG", u"(Hausa) ﻩَﻮُﺳَ", 1, u"(Hausa) ﻩَﻮُﺳَ", 1, "Hausa", 1, "hau")
        value = _get_anglicized_language_name(row)
        self.assertEqual(value, row[8])

    def test_found_invalid_xname(self):
        row = ("hi", u"(Hausa) هَوُسَ", "", "NG", u"(Hausa) ﻩَﻮُﺳَ", 1, u"(Hausa) ﻩَﻮُﺳَ", 1, "!ADDL", 1, "hau")
        value = _get_anglicized_language_name(row)
        self.assertEqual(value, "")
