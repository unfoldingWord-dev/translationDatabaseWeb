import datetime
import json

from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase
from django.utils import timezone

import requests_mock

from td.models import Language
from td.publishing.models import (
    OfficialResource, OfficialResourceType, PublishRequest)
from td.publishing.views import resource_language_json


class ResourceLanguageJsonTestCase(TestCase):

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
            requestor=self.user,
            resource_type=self.resource_type,
            language=self.language,
            checking_level=3,
            source_text=self.language,
            source_version='1.3.2',
            contributors="requestor: Test User,\ncontributors: Users",
            approved_at=now_dt,
        )

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
