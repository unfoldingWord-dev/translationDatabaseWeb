import json
import os

from django.test import TestCase

from mock import patch, Mock

from td.imports.models import WikipediaISOLanguage, EthnologueCountryCode, EthnologueLanguageCode, SIL_ISO_639_3

from ..exports import LanguageCodesExport, LanguageNamesExport


class ExportTests(TestCase):

    fixtures = ["additional-languages.json"]

    @classmethod
    def setUpClass(cls):
        wikipedia = open(os.path.join(os.path.dirname(__file__), "../imports/tests/data/wikipedia.html")).read()  # noqa
        ethno = open(os.path.join(os.path.dirname(__file__), "../imports/tests/data/LanguageCodes.tab")).read()  # noqa
        country = open(os.path.join(os.path.dirname(__file__), "../imports/tests/data/CountryCodes.tab")).read()  # noqa
        sil = open(os.path.join(os.path.dirname(__file__), "../imports/tests/data/iso_639_3.tab")).read()  # noqa
        with patch("td.imports.models.requests") as mock_requests:
            mock_requests.get.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = wikipedia
            WikipediaISOLanguage.reload()
            mock_response.content = ethno
            EthnologueLanguageCode.reload()
            mock_response.content = country
            EthnologueCountryCode.reload()
            mock_response.content = sil
            SIL_ISO_639_3.reload()

    def test_codes_export(self):
        data = LanguageCodesExport().text.split(" ")
        self.assertFalse("bmy" in data)
        self.assertTrue("aa" in data)
        self.assertTrue("kmg" in data)
        self.assertTrue("es-419" in data)

    def test_names_export(self):
        data = LanguageNamesExport().text.split("\n")
        data = [x.split("\t")[0] for x in data]
        self.assertFalse("bmy" in data)
        self.assertTrue("aa" in data)
        self.assertTrue("kmg" in data)
        self.assertTrue("es-419" in data)

    def test_names_json_export(self):
        data = json.loads(LanguageNamesExport().json)
        langs = {x["lc"]: x for x in data}
        self.assertFalse("bmy" in langs)
        self.assertTrue("aa" in langs)
        self.assertEquals(langs["aa"]["cc"], ["ET"])
        self.assertEquals(langs["aa"]["ln"], "Afaraf")
        self.assertEquals(langs["aa"]["lr"], "Africa")
        self.assertTrue("kmg" in langs)
        self.assertEquals(langs["kmg"]["cc"], ["PG"])
        self.assertEquals(langs["kmg"]["ln"], u"K\xe2te")
        self.assertEquals(langs["kmg"]["lr"], "Pacific")
        self.assertTrue("es-419" in langs)
        self.assertEquals(langs["es-419"]["cc"], [""])
        self.assertEquals(langs["es-419"]["ln"], u"Espa\xf1ol Latin America")
        self.assertEquals(langs["es-419"]["lr"], "")
