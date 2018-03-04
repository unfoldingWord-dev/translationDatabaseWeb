from django.test import TestCase

from mock import patch, Mock

from td.models import Language, JSONData
from td.tasks import reset_langnames_cache, update_langnames_data, post_to_ext_app, notify_external_apps
from td.tests.models import NoSignalTestCase


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
        self.assertIn("hc", json)


class PostToExtAppTestCase(TestCase):
    def setUp(self):
        self.patcher_post = patch("td.tasks.requests.post")
        self.patcher_send_mail = patch("td.tasks.send_mail")
        self.mock_post = self.patcher_post.start()
        self.mock_send_mail = self.patcher_send_mail.start()
        self.mock_response = Mock()
        self.mock_post.return_value = self.mock_response

    def tearDown(self):
        self.patcher_post.stop()
        self.patcher_send_mail.stop()

    def test_accepted_with_no_message(self):
        """
        If response is 202 and message is empty, function should return early without sending email
        """
        response = {"status_code": 202, "content": ""}
        self.mock_response.configure_mock(**response)

        post_to_ext_app("fake_url", "fake_data", "fake_headers")

        self.mock_post.assert_called_once_with("fake_url", data="fake_data", headers="fake_headers")
        self.assertFalse(self.mock_send_mail.called)

    def test_accepted_with_message(self):
        """
        If response is 202 but there is a message, function should send an email
        """
        response = {"status_code": 202, "content": "something's wrong"}
        self.mock_response.configure_mock(**response)

        post_to_ext_app("fake_url", "fake_data", "fake_headers")

        self.mock_post.assert_called_once_with("fake_url", data="fake_data", headers="fake_headers")
        self.assertEqual(self.mock_send_mail.call_count, 1)

    def test_not_accepted(self):
        """
        If response is not 202, functions should send an email regardless of the message
        """
        response = {"status_code": 403}
        self.mock_response.configure_mock(**response)

        post_to_ext_app("fake_url", "fake_data", "fake_headers")

        self.mock_post.assert_called_once_with("fake_url", data="fake_data", headers="fake_headers")
        self.assertEqual(self.mock_send_mail.call_count, 1)


class NotifyExternalAppTestCase(NoSignalTestCase):
    def setUp(self):
        super(NotifyExternalAppTestCase, self).setUp()

    def tearDown(self):
        super(NotifyExternalAppTestCase, self).tearDown()

    def test_called_inappropriately(self):
        """
        If called inappropriately, function should throw a fail response with message
        """
        status = notify_external_apps()
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance="string")
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance=1)
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance=[])
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance={})
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance=())
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance=object())
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        lang = Language()

        status = notify_external_apps(instance=lang)
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance=lang, action=None)
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance=lang, action=" ")
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance=lang, action=1)
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance=lang, action=[])
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance=lang, action={})
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance=lang, action=())
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance=lang, action=object())
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

    def test_unsupported_action(self):
        """
        If called with invalid/unsupported action, function should return early with fail status and a message
        """
        lang, _ = Language.objects.get_or_create(name="Test Language", code="text-x-lang")

        status = notify_external_apps(instance=lang, action="TEST")
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance=lang, action="DELETE")
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        status = notify_external_apps(instance=lang, action="CREATE")
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

    @patch("td.tasks.settings")
    def test_bad_ext_app_setting(self, mock_settings):
        """
        If external app setting is not a list, function should return early with a message
        """
        lang, _ = Language.objects.get_or_create(name="Test Language", code="text-x-lang")
        mock_settings.configure_mock(**{"EXT_APP_PUSH": None})

        status = notify_external_apps(instance=lang, action="UPDATE")
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        mock_settings.configure_mock(**{"EXT_APP_PUSH": {}})

        status = notify_external_apps(instance=lang, action="UPDATE")
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        mock_settings.configure_mock(**{"EXT_APP_PUSH": ()})

        status = notify_external_apps(instance=lang, action="UPDATE")
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        mock_settings.configure_mock(**{"EXT_APP_PUSH": " "})

        status = notify_external_apps(instance=lang, action="UPDATE")
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        mock_settings.configure_mock(**{"EXT_APP_PUSH": 1})

        status = notify_external_apps(instance=lang, action="UPDATE")
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

        mock_settings.configure_mock(**{"EXT_APP_PUSH": 1.0})

        status = notify_external_apps(instance=lang, action="UPDATE")
        self.assertFalse(status.success)
        self.assertGreater(len(status.message), 0)

    @patch("td.tasks.settings")
    @patch("td.tasks.post_to_ext_app.delay")
    def test_no_ext_apps(self, mock_async_post, mock_settings):
        """
        If called with the right arguments but no ext apps, function should return success status and post should
        not be called
        """
        lang, _ = Language.objects.get_or_create(name="Test Language", code="text-x-lang")
        mock_settings.configure_mock(**{"EXT_APP_PUSH": []})

        status = notify_external_apps(instance=lang, action="UPDATE")
        self.assertTrue(status.success)
        self.assertFalse(mock_async_post.called)

    @patch("td.tasks.settings")
    @patch("td.tasks.post_to_ext_app.delay")
    def test_with_ext_apps(self, mock_async_post, mock_settings):
        """
        If called with the right arguments and ext app settings, function should return success status, no message
        and post should be called for each of the item in the ext app settings.
        """
        lang, _ = Language.objects.get_or_create(name="Test Language", code="text-x-lang")
        app1 = {"url": "fakeUrl", "key": "fakeKey"}
        mock_settings.configure_mock(**{"EXT_APP_PUSH": [app1]})

        status = notify_external_apps(instance=lang, action="UPDATE")
        self.assertTrue(status.success)
        self.assertEqual(len(status.message), 0)
        self.assertEqual(mock_async_post.call_count, 1)

        mock_async_post.reset_mock()
        app2 = {"url": "fakeUrl"}
        mock_settings.configure_mock(**{"EXT_APP_PUSH": [app1, app2]})

        status = notify_external_apps(instance=lang, action="UPDATE")
        self.assertTrue(status.success)
        self.assertEqual(len(status.message), 0)
        self.assertEqual(mock_async_post.call_count, 2)
