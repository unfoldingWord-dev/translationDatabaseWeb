# coding: utf-8
from django.test import TestCase

from ..models import WikipediaISOLanguage, SIL_ISO_639_3


class WikipediaTestCase(TestCase):

    def test_string_representation(self):
        wiki = WikipediaISOLanguage(
            language_family="Northwest Caucasia",
            language_name="Abkhaz",
            native_name="аҧсуа бызшәа, аҧсшәа",
            iso_639_1="ab"
        )
        self.assertEquals(str(wiki), "Abkhaz")


class SIL_ISO_639_3TestCase(TestCase):

    def test_string_representation(self):
        sil = SIL_ISO_639_3(
            code="aaa",
            scope="I",
            language_type="L",
            ref_name="Ghotuo"
        )
        self.assertEquals(str(sil), "aaa")
