import json
import os

from django.core import management
from django.test import TestCase
from django.core.urlresolvers import reverse

from mock import patch

from td.imports.models import WikipediaISOLanguage, EthnologueCountryCode, EthnologueLanguageCode, SIL_ISO_639_3, WikipediaISOCountry

from td.models import Language, AdditionalLanguage, TempLanguage
from td.resources.models import Questionnaire
from td.tasks import integrate_imports, update_countries_from_imports


class TempLanguageTestCase(TestCase):

    def setUp(self):
        self.obj = TempLanguage(code="qaa-x-abcdef")
        self.obj.save()
        self.language = Language.objects.create(code = "test")
        self.questions = Questionnaire.objects.create(language=self.language, questions="""
        [
            {
               'id': 0,
               'text': 'What do you call your language?',
               'help': 'Test help text',
               'required': true,
               'input_type': 'string',
               'sort': 1,
               'depends_on': null
            }
        ]""")
        self.obj.questionnaire=self.questions
        self.obj.answers="""
        [
            'question_id':'0',
            'answer': 'wonderful'
        ]
        """

    def test_string_representation(self):
        """ __str__() should returned the model's code """
        self.assertEquals(str(self.obj), "qaa-x-abcdef")

    def test_get_absolute_url(self):
        """ get_absolute_url should return the URL to the detail page """
        self.assertEquals(self.obj.get_absolute_url(), reverse("templanguage_detail", args=[str(self.obj.id)]))

    def test_lang_assigned_url_property(self):
        """ lang_assigned_url should return the URL to the detail page of model's lang_assigned related object """
        self.assertEquals(self.obj.lang_assigned_url, reverse("language_detail", args=[str(self.obj.lang_assigned_id)]))

    def test_name_property(self):
        """ object.name should return its code """
        self.assertEquals(self.obj.name, "qaa-x-abcdef")

    def test_pending_method(self):
        """ object.pending should return a list of objects with status 'p' """
        returned = self.obj.pending()
        self.assertEqual(len(returned), 1)
        self.assertIn(self.obj, returned)

    def test_approved_method(self):
        """ object.approved should return a list of objects with status 'a' """
        self.assertEqual(len(self.obj.approved()), 0)
        a = TempLanguage(code="qaa-x-ghijkl", status="a")
        a.save()
        returned = self.obj.approved()
        self.assertEqual(len(returned), 1)
        self.assertIn(a, returned)

    def test_rejected_method(self):
        """ object.rejected should return a list of objects with status 'r' """
        self.assertEqual(len(self.obj.rejected()), 0)
        r = TempLanguage(code="qaa-x-ghijkl", status="r")
        r.save()
        returned = self.obj.rejected()
        self.assertEqual(len(returned), 1)
        self.assertIn(r, returned)

    def test_lang_assigned_map_method(self):
        """ lang_assigned_map should return a list of dictionary of object.code: object.lang_assigned.code """
        self.assertListEqual(self.obj.lang_assigned_map(), [{"qaa-x-abcdef": "qaa-x-abcdef"}])
        TempLanguage(code="qaa-x-123456").save()
        returned = self.obj.lang_assigned_map()
        self.assertEquals(len(returned), 2)
        self.assertIn({"qaa-x-abcdef": "qaa-x-abcdef"}, returned)
        self.assertIn({"qaa-x-123456": "qaa-x-123456"}, returned)

    def test_lang_assigned_changed_map(self):
        """ lang_assigned_map should return a list of dictionary of object.code: object.lang_assigned.code """
        l = self.obj.lang_assigned
        l.code = "abc"
        l.save()
        self.assertListEqual(self.obj.lang_assigned_changed_map(), [{"qaa-x-abcdef": "abc"}])

    def test_questions_answers(self):
        tmp = self.obj.questions_and_answers
        self.assertEqual(tmp[0]["id"],0)
        pass


class AdditionalLanguageTestCase(TestCase):

    def test_updated_at_set_on_save(self):
        additional = AdditionalLanguage.objects.create(
            ietf_tag="ttt-x-ismai",
            common_name="Ismaili"
        )
        first_updated_at = additional.updated_at
        additional.save()
        self.assertTrue(additional.updated_at > first_updated_at)

    def test_string_representation(self):
        additional = AdditionalLanguage(
            ietf_tag="ttt-x-ismai",
            common_name="Ismaili"
        )
        self.assertEquals(str(additional), "ttt-x-ismai")


class LanguageIntegrationTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(LanguageIntegrationTests, cls).setUpClass()
        wikipedia = open(os.path.join(os.path.dirname(__file__), "../imports/tests/data/wikipedia.html")).read()  # noqa
        ethno = open(os.path.join(os.path.dirname(__file__), "../imports/tests/data/LanguageCodes.tab")).read()  # noqa
        country = open(os.path.join(os.path.dirname(__file__), "../imports/tests/data/CountryCodes.tab")).read()  # noqa
        sil = open(os.path.join(os.path.dirname(__file__), "../imports/tests/data/iso_639_3.tab")).read()  # noqa
        w_country = open(os.path.join(os.path.dirname(__file__), "../imports/tests/data/wikipedia_country.html")).read()
        with patch("requests.Session") as mock_requests:
            mock_requests.get().status_code = 200
            mock_requests.get().content = wikipedia
            WikipediaISOLanguage.reload(mock_requests)
            mock_requests.get().content = ethno
            EthnologueLanguageCode.reload(mock_requests)
            mock_requests.get().content = country
            EthnologueCountryCode.reload(mock_requests)
            mock_requests.get().content = sil
            SIL_ISO_639_3.reload(mock_requests)
            mock_requests.get().content = w_country
            WikipediaISOCountry.reload(mock_requests)

        management.call_command("loaddata", "additional-languages.json", verbosity=1, noinput=True)
        management.call_command("loaddata", "uw_region_seed.json", verbosity=1, noinput=True)
        update_countries_from_imports()  # run task synchronously here
        integrate_imports()  # run task synchronously here

    def test_codes_export(self):
        data = Language.codes_text().split(" ")
        # self.assertFalse("bmy" in data)
        self.assertTrue("aa" in data)
        self.assertTrue("kmg" in data)
        self.assertTrue("es-419" in data)

    def test_names_export(self):
        data = Language.names_text().split("\n")
        data = [x.split("\t")[0] for x in data]
        # self.assertFalse("bmy" in data)
        self.assertTrue("aa" in data)
        self.assertTrue("kmg" in data)
        self.assertTrue("es-419" in data)

    def test_names_json_export(self):
        data = json.loads(json.dumps(Language.names_data()))
        langs = {x["lc"]: x for x in data}
        # self.assertFalse("bmy" in langs)
        self.assertTrue("aa" in langs)
        self.assertEquals(langs["aa"]["cc"], ["ET"])
        self.assertEquals(langs["aa"]["ln"], "Afaraf")
        self.assertEquals(langs["aa"]["lr"], "Africa")
        self.assertEquals(langs["aa"]["ld"], "ltr")
        self.assertTrue("kmg" in langs)
        self.assertEquals(langs["kmg"]["cc"], ["PG"])
        self.assertEquals(langs["kmg"]["ln"], u"K\xe2te")
        self.assertEquals(langs["kmg"]["lr"], "Pacific")
        self.assertEquals(langs["kmg"]["ld"], "ltr")
        self.assertTrue("es-419" in langs)
        self.assertEquals(langs["es-419"]["cc"], [])
        self.assertEquals(langs["es-419"]["ln"], u"Espa\xf1ol Latin America")
        self.assertEquals(langs["es-419"]["lr"], "")
        self.assertEquals(langs["es-419"]["ld"], "ltr")

    def test_three_letter_field(self):
        additional = AdditionalLanguage(
            two_letter="z3",
            common_name="ZTest of 3 Letters",
            three_letter="z3z",
            ietf_tag="z3-test"
        )
        additional.save()
        lang = Language.objects.get(code="z3")
        self.assertEquals(lang.iso_639_3, additional.three_letter)

    def test_add_and_delete_from_additionallanguage(self):
        additional = AdditionalLanguage.objects.create(
            ietf_tag="zzz-z-test",
            common_name="ZTest"
        )
        additional.save()
        integrate_imports()   # run task synchronously
        data = Language.names_text().split("\n")
        self.assertTrue("zzz-z-test\tZTest" in data)
        additional.delete()
        data = Language.names_text().split("\n")
        self.assertTrue("zzz-z-test\tZTest" not in data)

    def test_additionallanguage_direction(self):
        additional = AdditionalLanguage.objects.create(
            ietf_tag="zzz-r-test",
            common_name="ZRTest",
            direction="r"
        )
        additional.save()
        langnames = Language.names_text().split("\n")
        self.assertTrue("zzz-r-test\tZRTest" in langnames)
        data = json.loads(json.dumps(Language.names_data()))
        langs = {x["lc"]: x for x in data}
        self.assertTrue("zzz-r-test" in langs)
        self.assertEquals(langs["zzz-r-test"]["ld"], "rtl")


class LanguageTestCase(TestCase):

    def setUp(self):
        Language.objects.create(code="tl", name="Test Language")

    def test_names_data_short(self):
        """
        Only specified attributes should be returned by names_data (short version)
        """
        result = Language.names_data(short=True)
        self.assertEqual(len(result), 1)
        self.assertIn("pk", result[0])
        self.assertIn("lc", result[0])
        self.assertIn("ln", result[0])
        self.assertIn("ang", result[0])
        self.assertIn("lr", result[0])
        self.assertNotIn("alt", result[0])
        self.assertNotIn("ld", result[0])
        self.assertNotIn("gw", result[0])
        self.assertEqual(result[0].get("lc"), "tl")
        self.assertEqual(result[0].get("ln"), "Test Language")

    def test_names_data(self):
        """
        Default version of Language.names_data should contain more attributes
        """
        result = Language.names_data()
        self.assertEqual(len(result), 1)
        self.assertIn("alt", result[0])
        self.assertIn("ld", result[0])
        self.assertIn("gw", result[0])
        self.assertIn("cc", result[0])
