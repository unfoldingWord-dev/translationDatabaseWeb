from django.test import TestCase

from mock import patch

from ..models import Language, JSONData
from ..tasks import reset_langnames_cache, update_langnames_data


class ResetLangnamesCacheTestCase(TestCase):

    def setUp(self):
        Language.objects.create(code="tl", name="Test Language")

    def test_reset_langnames_cache_short(self):
        """
        Short version of reset_langnames_cache should only contain limited info and not include CC and ALT attributes
        """
        with patch("td.tasks.cache") as mock_cache:
            cache = {}

            def get(key, default=None):
                return cache.get(key, default)

            def _set(key, value, timeout=None):
                cache[key] = value

            mock_cache.get = get
            mock_cache.set = _set

            reset_langnames_cache(short=True)
            result = cache["langnames_short"][0]

            self.assertIs(cache["langnames_short_fetching"], False)
            self.assertIn("pk", result)
            self.assertIn("lc", result)
            self.assertIn("ln", result)
            self.assertIn("lr", result)
            self.assertIn("ang", result)
            self.assertNotIn("cc", result)
            self.assertNotIn("alt", result)
            self.assertEqual(result["lc"], "tl")
            self.assertEqual(result["ln"], "Test Language")

    def test_reset_langnames_cache(self):
        """
        Default version of reset_langnames_cache should return all info needed for langnames.json
        """
        with patch("td.tasks.cache") as mock_cache:
            cache = {}

            def get(key, default=None):
                return cache.get(key, default)

            def _set(key, value, timeout=None):
                cache[key] = value

            mock_cache.get = get
            mock_cache.set = _set

            reset_langnames_cache()
            result = cache["langnames"][0]

            self.assertIs(cache["langnames_fetching"], False)
            self.assertIn("pk", result)
            self.assertIn("lc", result)
            self.assertIn("ln", result)
            self.assertIn("lr", result)
            self.assertIn("ld", result)
            self.assertIn("cc", result)
            self.assertIn("gw", result)
            self.assertIn("ang", result)
            self.assertIn("alt", result)
            self.assertEqual(result["lc"], "tl")
            self.assertEqual(result["ln"], "Test Language")


class UpdateLangnamesDataTestCase(TestCase):
    def setUp(self):
        Language.objects.create(code="tl", name="Test Language")

    def test_update_langnames_data(self):
        """
        After update_langnames_data() is called, there should be one JSONData object created called "langnames", which
        content has the expected attributes.
        """
        update_langnames_data()
        result = JSONData.objects.filter(name="langnames")
        json = result[0].data[0]
        self.assertEqual(len(result), 1)
        self.assertIn("pk", json)
        self.assertIn("lc", json)
        self.assertIn("ln", json)
        self.assertIn("ang", json)
        self.assertIn("alt", json)
        self.assertIn("lc", json)
        self.assertIn("lr", json)
        self.assertIn("gw", json)
        self.assertIn("ld", json)
