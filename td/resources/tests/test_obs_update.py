from django.db import transaction
from django.test import TestCase
from mock import patch

from td.commenting.models import CommentTag
from ..models import Resource
from td.models import Language
from ..tasks import _process_obs_response
from pinax.eventlog.models import Log


GOOD_JSON_DATA = [{"date_modified": "20141208",
                   "direction": "ltr",
                   "language": "zt1",
                   "status": {
                       "checking_entity": "translation team",
                       "checking_level": "1",
                       "comments": "Level 1 check cleared via email to Test User by translation team.",
                       "contributors": "tuser;testy2user",
                       "publish_date": "2014-12-08",
                       "source_text": "en",
                       "source_text_version": "3.1",
                       "version": "3.2.1"
                   },
                   "string": "Espa\u00f1ol"},
                  {"date_modified": "20141208",
                   "direction": "ltr",
                   "language": "zt2",
                   "status": {
                       "checking_entity": "translation team",
                       "checking_level": "1",
                       "comments": "",
                       "contributors": "testuser42;test-user;testing",
                       "publish_date": "2014-12-08",
                       "source_text": "en",
                       "source_text_version": "3.1",
                       "version": "3.2.1"},
                   "string": "Fran\u00e7ais"}]


class OBSTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(OBSTestCase, cls).setUpClass()
        Language.objects.get_or_create(code="zt1", name="Z Test 1")
        Language.objects.get_or_create(code="zt2", name="Z Test 2")

    def test_good_obs_fetch(self):
        Resource.objects.all().delete()
        self.assertEquals(Resource.objects.all().count(), 0)
        with patch("requests.Response") as mock_response:
            mock_response.status_code = 200
            mock_response.json.return_value = GOOD_JSON_DATA
            _process_obs_response(mock_response)
            self.assertEquals(Resource.objects.count(), len(GOOD_JSON_DATA))

    def test_bad_obs_fetch(self):
        Resource.objects.all().delete()
        self.assertEquals(Resource.objects.all().count(), 0)
        with patch("requests.Response") as mock_response:
            mock_response.status_code = 404
            mock_response.content = ""
            _process_obs_response(mock_response)
            self.assertEquals(Resource.objects.all().count(), 0)
            self.assertTrue(Log.objects.filter(action="GET_OBS_CATALOG_FAILED").exists())
