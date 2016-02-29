from django.test import TestCase

from mock import patch

from ..models import Language
from ..tasks import reset_langnames_cache


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
            # self.assertNotIn("alt", result)
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
            # self.assertIn("alt", result)
            self.assertEqual(result["lc"], "tl")
            self.assertEqual(result["ln"], "Test Language")
