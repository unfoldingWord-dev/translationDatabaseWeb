# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User

from mock import patch

from td.models import Language
from td.publishing.models import (
    OfficialResource, OfficialResourceType, PublishRequest)


class PublishRequestTestCase(TestCase):

    def setUp(self):
        resource_type, _ = OfficialResourceType.objects.get_or_create(
            short_name="obs",
            long_name="OpenBibleStory"
        )
        language, _ = Language.objects.get_or_create(
            code="en",
            name="English"
        )
        source_language, _ = Language.objects.get_or_create(
            code="arc",
            name="Aramaic"
        )
        self.user, _ = User.objects.get_or_create(
            first_name="Test",
            last_name="RequestorUser",
            username="test_requestor_user"
        )
        self.model, _ = PublishRequest.objects.get_or_create(
            requestor="Test publish request",
            resource_type=resource_type,
            language=language,
            checking_level=1,
            source_text=source_language
        )

    @patch("td.publishing.models.OfficialResource.ingest")
    def test_publish(self, mock_ingest):
        resource = self.model.publish(by_user=self.user)
        self.assertIsInstance(resource, OfficialResource)
        self.assertEqual(resource.language.code, "en")
        mock_ingest.assert_called_once_with(publish_request=self.model)

    @patch("td.publishing.models.OfficialResource.ingest")
    def test_publish_unicode_notes(self, mock_ingest):
        r = PublishRequest.objects.create(
            requestor="Wendy Colón",
            resource_type=self.model.resource_type,
            language=self.model.language,
            checking_level=1,
            source_text=self.model.source_text,
            contributors="""Wendy Colón
Aida Rodríguez
Ada González
Miriam Planas"""
        )
        r = PublishRequest.objects.get(pk=r.pk)
        resource = r.publish(by_user=self.user)
        self.assertIsInstance(resource, OfficialResource)
        self.assertEqual(resource.language.code, "en")
        mock_ingest.assert_called_once_with(publish_request=r)
