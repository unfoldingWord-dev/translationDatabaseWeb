from django.test import TestCase
from td.models import Country, Language
from ..tasks import seed_languages_gateway_language


class SeedGatewayTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(SeedGatewayTestCase, cls).setUpClass()
        country1 = Country(code="c1", name="Country 1")
        country1.extra_data = {"gateway_language": "gz1"}
        country1.save()
        country2 = Country(code="c2", name="Country 2")
        country2.save()
        lang1 = Language(code="gz1", name="Z Test 1", gateway_flag=True, gateway_language=None, country=country1)
        lang1.save()
        lang2 = Language(code="gz2", name="Z Test 2", gateway_flag=False, gateway_language=lang1, country=country2)
        lang2.save()
        lang3 = Language(code="gz3", name="Z Test 3", gateway_flag=False, gateway_language=None, country=country1)
        lang3.save()
        lang4 = Language(code="gz4", name="Z Test 4", gateway_flag=False, gateway_language=None, country=country2)
        lang4.save()
        lang5 = Language(code="gz5", name="Z Test 5", gateway_flag=False, gateway_language=None, country=None)
        lang5.save()

    def test_seed(self):
        seed_languages_gateway_language()
        z1 = Language.objects.get(code="gz1")
        self.assertIsNone(z1.gateway_language)
        self.assertEquals(Language.objects.get(code="gz2").gateway_language, z1)
        self.assertEquals(Language.objects.get(code="gz3").gateway_language, z1)
        self.assertIsNone(Language.objects.get(code="gz4").gateway_language)
        self.assertIsNone(Language.objects.get(code="gz5").gateway_language)
