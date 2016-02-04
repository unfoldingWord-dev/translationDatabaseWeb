from __future__ import absolute_import

import subprocess

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from celery import task

from .models import PublishRequest


@task()
def publish(langcode):
    subprocess.call(["/var/www/vhosts/door43.org/tools/uw/publish.sh", "-l", langcode])


@task()
def send_request_email(request_id):
    notify_requestor_received.delay(request_id)
    pr = PublishRequest.objects.get(pk=request_id)
    html_contents = render_to_string("./email/publishrequest_notify_html.html", {"publish_request": pr})
    plain_contents = render_to_string("./email/publishrequest_notify_plain.html", {"publish_request": pr})
    send_mail("Publish Request #{0}".format(str(pr.pk)),
              plain_contents,
              settings.EMAIL_FROM,
              settings.EMAIL_NOTIFY_LIST,
              html_message=html_contents)


@task()
def notify_requestor_received(request_id):
    pr = PublishRequest.objects.get(pk=request_id)
    html_contents = render_to_string("./email/notify_requestor_received_html.html", {"publish_request": pr})
    plain_contents = render_to_string("./email/notify_requestor_received_plain.html", {"publish_request": pr})
    send_mail("Publish Request #{0} Received".format(str(pr.pk)),
              plain_contents,
              settings.EMAIL_FROM,
              [pr.requestor_email],
              html_message=html_contents)


@task()
def notify_requestor_approved(request_id):
    pr = PublishRequest.objects.get(pk=request_id)
    html_contents = render_to_string("./email/notify_requestor_approved_html.html", {"publish_request": pr})
    plain_contents = render_to_string("./email/notify_requestor_approved_plain.html", {"publish_request": pr})
    send_mail("Publish Request #{0} Approved".format(str(pr.pk)),
              plain_contents,
              settings.EMAIL_FROM,
              [pr.requestor_email],
              html_message=html_contents)


@task()
def notify_requestor_rejected(request_id):
    pr = PublishRequest.objects.get(pk=request_id)
    html_contents = render_to_string("./email/notify_requestor_rejected_html.html", {"publish_request": pr})
    plain_contents = render_to_string("./email/notify_requestor_rejected_plain.html", {"publish_request": pr})
    send_mail("Publish Request #{0} Rejected".format(str(pr.pk)),
              plain_contents,
              settings.EMAIL_FROM,
              [pr.requestor_email],
              html_message=html_contents)


def approve_publish_request(request_id, user_id):
    pr = PublishRequest.objects.get(pk=request_id)
    user = User.objects.get(pk=user_id)
    oresource = pr.publish(by_user=user)
    notify_requestor_approved.delay(pr.pk)
    return oresource.pk


def reject_publish_request(request_id, user_id):
    pr = PublishRequest.objects.get(pk=request_id)
    user = User.objects.get(pk=user_id)
    pr.reject(by_user=user)
    notify_requestor_rejected.delay(pr.pk)
