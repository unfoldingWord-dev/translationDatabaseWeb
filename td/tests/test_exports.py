import json
import os

from django.test import TestCase

from mock import patch, Mock

from td.imports.models import WikipediaISOLanguage, SIL_ISO_639_3

from ..exports import LanguageCodesExport, LanguageNamesExport
from ..models import AdditionalLanguage


class ExportTests(TestCase):

    fixtures = ["additional-languages.json"]

    def setUp(self):
        wikipedia = open(os.path.join(os.path.dirname(__file__), "../imports/tests/data/wikipedia.html")).read()  # noqa
        sil = open(os.path.join(os.path.dirname(__file__), "../imports/tests/data/iso_639_3.tab")).read()  # noqa
        with patch("td.imports.models.requests") as mock_requests:
            mock_requests.get.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = wikipedia
            WikipediaISOLanguage.reload()
            mock_response.content = sil
            SIL_ISO_639_3.reload()
        self.expected_count = SIL_ISO_639_3.objects.filter(
            scope=SIL_ISO_639_3.SCOPE_INDIVIDUAL,
            language_type=SIL_ISO_639_3.TYPE_LIVING
        ).count() + AdditionalLanguage.objects.count()

    def test_codes_export(self):
        data = LanguageCodesExport().text
        self.assertEquals(len(data.split(", ")), self.expected_count)

    def test_names_export(self):
        data = LanguageNamesExport().text
        self.assertEquals(len(data.split("\n")), self.expected_count)

    def test_names_json_export(self):
        data = json.loads(LanguageNamesExport().json)
        self.assertEquals(len(data), self.expected_count)
