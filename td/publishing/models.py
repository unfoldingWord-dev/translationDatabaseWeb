from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

import reversion

from td.models import Language


class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name of Organization")
    email = models.CharField(max_length=255, blank=True, verbose_name="Email address")
    phone = models.CharField(max_length=255, blank=True, verbose_name="Phone number")
    website = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    languages = models.ManyToManyField(Language, related_name="organizations")
    other = models.TextField(blank=True, verbose_name="Other information")
    checking_entity = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name of contact")
    email = models.CharField(max_length=255, blank=True, verbose_name="Email address")
    d43username = models.CharField(max_length=255, blank=True, verbose_name="Door43 username")
    location = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True, verbose_name="Phone number")
    languages = models.ManyToManyField(Language, related_name="contacts")
    org = models.ManyToManyField(Organization, blank=True, verbose_name="organizations")
    other = models.TextField(blank=True, verbose_name="Other information")

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name


class ConnectionType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name of Connection Type")
    mutual = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name


class Connection(models.Model):
    con_src = models.ForeignKey(Contact, related_name="source_connections")
    con_dst = models.ForeignKey(Contact, related_name="destination_connections", verbose_name="Connection")
    con_type = models.ForeignKey(ConnectionType, verbose_name="Type")

    class Meta:
        ordering = ["con_src"]

    def __unicode__(self):
        return self.con_src.name


class RecentCommunication(models.Model):
    contact = models.ForeignKey(Contact, related_name="recent_communications")
    communication = models.TextField(blank=True, verbose_name="Message")
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        ordering = ["contact", "created"]

    def __unicode__(self):
        return self.contact.name


CHECKING_LEVEL_CHOICES = [
    (1, "1"),
    (2, "2"),
    (3, "3"),
]


@python_2_unicode_compatible
class OfficialResourceType(models.Model):
    short_name = models.CharField(max_length=5, help_text="a 5 character identification code")
    long_name = models.CharField(max_length=50, help_text="a more descriptive name")
    description = models.TextField(blank=True)

    def __str__(self):
        return "({0}) {1}".format(self.short_name, self.long_name)


@reversion.register()
class OfficialResource(models.Model):
    language = models.ForeignKey(Language, related_name="official_resources", verbose_name="Language")
    resource_type = models.ForeignKey(OfficialResourceType, verbose_name="official_resources")
    contact = models.ForeignKey(Contact, related_name="official_resources", null=True, blank=True)
    date_started = models.DateField()
    notes = models.TextField(blank=True)
    offline = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    # Publishing
    publish_date = models.DateField(null=True, blank=True)
    version = models.CharField(max_length=10, blank=True)
    source_text = models.ForeignKey(Language, null=True, blank=True, related_name="+")
    source_version = models.CharField(max_length=10, blank=True)
    checking_entity = models.ManyToManyField(Organization, related_name="resource_publications", blank=True)
    contributors = models.ManyToManyField(Contact, related_name="+", blank=True)
    checking_level = models.IntegerField(choices=CHECKING_LEVEL_CHOICES, null=True, blank=True)

    def versions(self):
        return reversion.get_for_object(self)

    class Meta:
        ordering = ["language", "contact"]

    def __unicode__(self):
        return self.language.code


class Comment(models.Model):
    official_resource = models.ForeignKey(OfficialResource, related_name="comments", null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)


@python_2_unicode_compatible
class PublishRequest(models.Model):
    requestor = models.CharField(max_length=100)
    resource_type = models.ForeignKey(OfficialResourceType, null=True)
    language = models.ForeignKey(Language, related_name="publish_requests")
    checking_level = models.IntegerField(choices=CHECKING_LEVEL_CHOICES)
    source_text = models.ForeignKey(Language, related_name="source_publish_requests", null=True)
    source_version = models.CharField(max_length=10, blank=True)
    contributors = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(default=None, blank=True, null=True, db_index=True)
    requestor_email = models.EmailField(blank=True, default="", help_text="email address to be notified of request status")

    def __str__(self):
        return "({0}) for {1} in language: {2}".format(str(self.pk), str(self.get_resource_display()), self.language)


class LicenseAgreement(models.Model):
    publish_request = models.ForeignKey(PublishRequest)
    document = models.FileField(upload_to="agreements/")
