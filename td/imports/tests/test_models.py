# coding: utf-8
from django.test import TestCase

from ..models import (
    EthnologueCountryCode,
    EthnologueLanguageCode,
    EthnologueLanguageIndex,
    SIL_ISO_639_3,
    WikipediaISOLanguage,
    WikipediaISOCountry
)


class EthnologueLanguageCodeTestCase(TestCase):

    def test_string_representation(self):
        ethno = EthnologueLanguageCode(
            code="zzj",
            country_code="CN",
            status=EthnologueLanguageCode.STATUS_LIVING,
            name="Zhuang, Zuojiang"
        )
        self.assertEquals(str(ethno), "zzj")


class EthnologueLanguageIndexTestCase(TestCase):

    def test_string_representation(self):
        ethno = EthnologueLanguageIndex(
            language_code="zzj",
            country_code="VN",
            name_type=EthnologueLanguageIndex.TYPE_LANGUAGE_ALTERNATE,
            name="Nung Chao"
        )
        self.assertEquals(str(ethno), "Nung Chao")


class EthnologueCountryCodeTestCase(TestCase):

    def test_string_representation(self):
        ethno = EthnologueCountryCode(
            code="ZW",
            name="Zimbabwe",
            area="Africa"
        )
        self.assertEquals(str(ethno), "ZW")


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


class WikipediaCountryTestCase(TestCase):

    def test_string_representation(self):
        wcountry = WikipediaISOCountry(
            alpha_2="ZZ",
            alpha_3="ZZZ",
            english_short_name="Z Test Country",
        )
        self.assertEquals(str(wcountry), "Z Test Country (ZZ) (ZZZ)")