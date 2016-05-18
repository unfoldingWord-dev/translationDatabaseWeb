from __future__ import absolute_import

import datetime
import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import TestCase, Client
from django.utils import timezone

import requests_mock

from td.models import Language
from td.publishing.models import OfficialResource, OfficialResourceType, PublishRequest
from td.publishing.views import resource_language_json, resource_catalog_json, redirect_new_publishing


class RedirectNewPublishingTestCase(TestCase):
    @requests_mock.mock()
    def test_redirect_new_publishing(self, request):
        response = redirect_new_publishing(request)
        self.assertEqual(response.status_code, 302)


class PublishingViewsBaseTestCase(TestCase):
    def setUp(self):
        now_dt = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
        # Create user
        self.user, _ = User.objects.get_or_create(
            first_name="Test",
            last_name="User",
            username="test_user",
        )
        self.user.set_password("test_password")
        self.user.save()
        # Create official resource type
        self.resource_type, _ = OfficialResourceType.objects.get_or_create(
            short_name="obs",
            long_name="Open Bible Story"
        )
        # Create language
        self.language, _ = Language.objects.get_or_create(
            code="en",
            name="English",
        )
        # Create official resource
        self.resource, _ = OfficialResource.objects.get_or_create(
            language=self.language,
            resource_type=self.resource_type,
            created_by=self.user,
            checking_level=3,
            date_started=now_dt,
            publish_date=now_dt,
            version="1.0",
        )
        # Create publish request
        self.pub_req, _ = PublishRequest.objects.get_or_create(
            requestor='Unit Tester',
            resource_type=self.resource_type,
            language=self.language,
            checking_level=3,
            source_text=self.language,
            source_version='1.3.2',
            contributors="requestor: Test User,\ncontributors: Users",
        )
        self.pub_req.save()
        # create a rejected request
        self.pub_rej, _ = PublishRequest.objects.get_or_create(
            requestor="Unit Tester",
            resource_type=self.resource_type,
            language=self.language,
            checking_level=3,
            source_text=self.language,
            source_version='1.3.2',
            contributors="requestor: Test User,\ncontributors: Users",
            rejected_at=now_dt,
            rejected_by=self.user
        )
        self.pub_rej.save()
        # create an approved request
        self.pub_approved_req, _ = PublishRequest.objects.get_or_create(
            requestor="Unit Tester",
            resource_type=self.resource_type,
            language=self.language,
            checking_level=3,
            source_text=self.language,
            source_version="1.3.2",
            contributors="requestor: Test User,\ncontributors: Users",
            approved_at=now_dt
        )
        self.pub_approved_req.save()


class ResourceLanguageJsonTestCase(PublishingViewsBaseTestCase):
    @requests_mock.mock()
    def test_chapters_and_meta(self, mock_requests):
        resp = resource_language_json(mock_requests, kind="obs", lang="en")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue("meta" in data)
        self.assertEqual(data["meta"], {})
        self.assertTrue("chapters" in data)
        self.assertEqual(data["chapters"], [])

    @requests_mock.mock()
    def test_official_resource_type_404(self, mock_requests):
        with self.assertRaises(Http404):
            resource_language_json(mock_requests, kind="foo", lang="en")

    @requests_mock.mock()
    def test_language_404(self, mock_requests):
        with self.assertRaises(Http404):
            resource_language_json(mock_requests, kind="obs", lang="bar")


class ResourceCatalogJsonTestCase(PublishingViewsBaseTestCase):
    @requests_mock.mock()
    def test_full_catalog_empty(self, mock_requests):
        expected = {
            "cat": [
                {
                    "langs": [],
                    "slug": "obs",
                    "title": "Open Bible Story",
                },
            ]
        }
        resp = resource_catalog_json(mock_requests, kind=None)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data, expected)

    @requests_mock.mock()
    def test_obs_catalog_empty(self, mock_requests):
        expected = {
            "cat": [
                {
                    "langs": [],
                    "slug": "obs",
                    "title": "Open Bible Story",
                },
            ]
        }
        resp = resource_catalog_json(mock_requests, kind="obs")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data, expected)


class OfficialResourceListViewTestCase(PublishingViewsBaseTestCase):
    def test_get_context_data(self):
        client = Client()
        client.login(username='test_user', password='test_password')

        response = client.get(reverse('oresource_list'))

        self.assertEqual(1, response.context_data['publish_requests'].count())
        self.assertEqual(1, response.context_data['rejected_requests'].count())


class PublishRequestResubmitViewTestCase(PublishingViewsBaseTestCase):
    def test_get_context_data(self):
        client = Client()
        response = client.get(reverse('publish_request_resubmit', args=[self.pub_req.permalink]))

        self.assertIsNotNone(response.context_data['publishrequest'])

        # check the permalink value to be sure it is the one we requested
        found_permalink = response.context_data['publishrequest'].permalink
        self.assertEqual(self.pub_req.permalink, found_permalink)

        # check the method for decoding the permalink back to the pk
        pk_from_permalink = PublishRequest.pk_from_permalink(found_permalink)
        self.assertEqual(self.pub_req.pk, pk_from_permalink)
