from django.test import TestCase
from django.contrib.auth.models import User

from mock import patch, Mock

from td.models import Language
from td.publishing.models import OfficialResourceType, PublishRequest
from td.publishing.tasks import approve_publish_request, reject_publish_request


class PublishTasksTestCase(TestCase):

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
            code="la",
            name="Latin"
        )
        self.user, _ = User.objects.get_or_create(
            first_name="Test",
            last_name="RequestorUser",
            username="test_requestor_user"
        )
        self.request, _ = PublishRequest.objects.get_or_create(
            requestor="Test publish request",
            resource_type=resource_type,
            language=language,
            checking_level=1,
            source_text=source_language
        )

    @patch("td.publishing.tasks.PublishRequest.publish")
    @patch("td.publishing.tasks.notify_requestor_approved")
    def test_approve_publish_request(self, mock_task, mock_publish):
        mock_publish.return_value = Mock(pk=1)
        resource_id = approve_publish_request(
            self.request.id,
            self.user.id
        )
        # Assert that the resource.id was returned...
        self.assertEqual(resource_id, 1)
        # and that the PublishRequst.publish was called with the user object...
        mock_publish.assert_called_once_with(by_user=self.user)
        # and the notify_requestor_approved celery task was called with the
        # PublishRequest.id
        mock_task.delay.assert_called_once_with(self.request.id)

    @patch("td.publishing.tasks.PublishRequest.reject")
    @patch("td.publishing.tasks.notify_requestor_rejected")
    def test_reject_publish_request(self, mock_task, mock_reject):
        reject_publish_request(
            self.request.id,
            self.user.id
        )

        # assert that the PublishRequst.reject was called with the user object...
        mock_reject.assert_called_once_with(by_user=self.user)
        # and the notify_requestor_rejected celery task was called with the
        # PublishRequest.id
        mock_task.delay.assert_called_once_with(self.request.id)
