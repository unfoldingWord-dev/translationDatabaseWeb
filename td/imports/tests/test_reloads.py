import os

from django.test import TestCase

from mock import patch, Mock

from ..models import WikipediaISOLanguage, SIL_ISO_639_3


class WikipediaReloadTests(TestCase):

    def setUp(self):
        self.data = open(os.path.join(os.path.dirname(__file__), "data/wikipedia.html")).read()

    def test_reload(self):
        with patch("td.imports.models.requests") as mock_requests:
            mock_requests.get.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = self.data
            WikipediaISOLanguage.reload()
            self.assertEquals(WikipediaISOLanguage.objects.count(), 184)


class SILISO639_3ReloadTests(TestCase):

    def setUp(self):
        self.data = open(os.path.join(os.path.dirname(__file__), "data/iso_639_3.tab")).read()

    def test_reload(self):
        with patch("td.imports.models.requests") as mock_requests:
            mock_requests.get.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = self.data
            SIL_ISO_639_3.reload()
            self.assertEquals(SIL_ISO_639_3.objects.count(), 7879)
