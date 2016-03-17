import base64
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from jsonfield import JSONField
from reversion import revisions as reversion

from td.models import Language
from td.publishing.resources import RESOURCE_TYPES


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

    def ingest(self, language, publish_request):
        ResourceIngestor = RESOURCE_TYPES.get(self.short_name)
        if ResourceIngestor:
            resource_ingestor = ResourceIngestor(language.code, publish_request)
            chapters = resource_ingestor.fetch_chapters()
            resource_doc = ResourceDocument()
            resource_doc.json_data = chapters
            resource_doc.publish_request = publish_request
            resource_doc.resource_type = publish_request.resource_type
            resource_doc.language = language
            resource_doc.save()

    @property
    def data(self):
        return [
            resource.data
            for resource in self.officialresource_set.order_by("language__code")
        ]

    def __str__(self):
        return "({0}) {1}".format(self.short_name, self.long_name)


@reversion.register()
class OfficialResource(models.Model):
    language = models.ForeignKey(Language, related_name="official_resources", verbose_name="Language")
    resource_type = models.ForeignKey(OfficialResourceType, verbose_name="Official resource type")
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

    def ingest(self, publish_request):
        self.resource_type.ingest(self.language, publish_request)

    @property
    def data(self):
        """
        {
            "date_modified": "20150826",
            "direction": "ltr",
            "language": "en",
            "status": {
                "checking_entity": "Distant Shores Media; Wycliffe Associates",
                "checking_level": "3",
                "comments": "Original source text.",
                "contributors": "Distant Shores Media",
                "publish_date": "2015-08-26",
                "source_text": "en",
                "source_text_version": "4",
                "version": "4"
            },
            "string": "English"
        }
        """
        return {
            "date_modified": self.created,
            "direction": self.language.get_direction_display(),
            "language": self.language.code,
            "string": self.language.name,
            "status": {
                "checking_entity": self.checking_entity.name if self.checking_entity else "",
                "checking_level": self.checking_level,
                "comments": "\n\n".join([
                    comment.comment
                    for comment in self.comments.order_by("created_at")
                ]),
                "contributors": ", ".join([
                    contact.name
                    for contact in self.contributors.order_by("name")
                ]),
                "publish_date": self.publish_date.strftime("%Y-%m-%d") if self.publish_date else "",
                "source_text": self.source_text.code if self.source_text else "",
                "source_text_version": self.source_version,
                "version": self.version
            }
        }

    def versions(self):
        return reversion.get_for_object(self)

    class Meta:
        ordering = ["language", "contact"]

    def __unicode__(self):
        return "({code}) {resource_type} {version}".format(
            code=self.language.code,
            resource_type=self.resource_type.long_name,
            version=self.version
        )


class Comment(models.Model):
    official_resource = models.ForeignKey(OfficialResource, related_name="comments", null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)


@python_2_unicode_compatible
class PublishRequest(models.Model):
    requestor = models.CharField(max_length=100, verbose_name="Requester name")
    resource_type = models.ForeignKey(OfficialResourceType, null=True, verbose_name='Official resource type')
    language = models.ForeignKey(Language, related_name="publish_requests")
    checking_level = models.IntegerField(choices=CHECKING_LEVEL_CHOICES, verbose_name="Requested checking level")
    source_text = models.ForeignKey(Language, related_name="source_publish_requests", null=True)
    source_version = models.CharField(max_length=10, blank=True)
    contributors = models.TextField(blank=True, help_text="Names or Pseudonyms")
    created_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(default=None, blank=True, null=True, db_index=True)
    requestor_email = models.EmailField(blank=True,
                                        default="",
                                        verbose_name="Requester email",
                                        help_text="email address to be notified of request status")
    license_title = models.TextField(default="CC BY-SA 4.0", blank=True, null=False)
    rejected_at = models.DateTimeField(default=None, null=True, blank=True, verbose_name="Rejected at")
    rejected_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=True, blank=True,
                                    verbose_name="Rejected by")

    @property
    def permalink(self):
        if self.pk is None:
            return None

        return base64.urlsafe_b64encode(unicode(self.pk).zfill(6))

    @property
    def version(self):
        parts = self.source_version.split(".")
        if len(parts) == 3:
            return ".".join([parts[0], str(int(parts[1]) + 1), parts[2]])
        else:
            return "invalid"

    @property
    def data(self):
        return {
            "mod": self.created_at.strftime("%s"),
            "direction": self.language.get_direction_display(),
            "lc": self.language.code,
            "name": self.language.name,
            "status": {
                "checking_entity": "",  # orgs aren't being added to resources
                "checking_level": self.checking_level,
                "contributors": self.contributors,
                "publish_date": self.approved_at.isoformat(),
                "source_text": self.source_text.code if self.source_text else "",
                "source_text_version": self.source_version,
                "version": self.version,
                "license": self.license_title,
            }
        }

    def publish(self, by_user):
        resource = self.resource_type.officialresource_set.create(
            created_by=by_user,
            language=self.language,
            checking_level=self.checking_level,
            source_text=self.source_text,
            source_version=self.source_version,
            version=self.version,
            notes="requestor: {0}\ncontributors: {1}".format(
                self.requestor.encode("utf-8"),
                self.contributors.encode("utf-8")
            ),
            date_started=self.created_at.date()
        )
        self.approved_at = timezone.now()
        self.save()
        resource.ingest(publish_request=self)
        return resource

    def reject(self, by_user):
        self.rejected_at = timezone.now()
        self.rejected_by = by_user
        self.save()

    def __str__(self):
        return "({0}) for {1} in language: {2}".format(str(self.pk), str(self.resource_type), self.language.code)

    @staticmethod
    def pk_from_permalink(permalink):
        try:
            if type(permalink) is unicode:
                decoded = base64.urlsafe_b64decode(permalink.encode('ascii', 'ignore'))
            else:
                decoded = base64.urlsafe_b64decode(permalink)
            return int(decoded)
        except (TypeError, Exception):
            return None


class LicenseAgreement(models.Model):
    publish_request = models.ForeignKey(PublishRequest)
    document = models.FileField(upload_to="agreements/")


class Chapter(models.Model):
    resource_type = models.ForeignKey(OfficialResourceType)
    publish_request = models.ForeignKey(PublishRequest, default=None, null=True)
    created = models.DateTimeField(default=timezone.now)
    language = models.ForeignKey(Language)
    number = models.IntegerField()
    ref = models.TextField(blank=True)
    title = models.TextField()

    @property
    def data(self):
        data = {
            "number": self.number,
            "title": self.title,
        }
        if self.ref:
            data["ref"] = self.ref

        frame_set = self.frame_set
        if self.resource_type.short_name == "obs":
            frame_set = frame_set.order_by("identifier")
        else:
            frame_set = frame_set.order_by("number", "id")
        data["frames"] = [fr.data for fr in frame_set]
        return data


class Frame(models.Model):
    chapter = models.ForeignKey(Chapter)
    identifier = models.TextField()
    number = models.IntegerField(default=None, null=True)
    ref = models.TextField(blank=True)
    title = models.TextField(blank=True)
    img = models.URLField()
    text = models.TextField()

    @property
    def data(self):
        data = {
            "id": self.identifier,
            "text": self.text,
        }
        if self.img:
            data["img"] = self.img
        if self.ref:
            data["ref"] = self.ref
        if self.title:
            data["title"] = self.title
        return data


class ResourceDocument(models.Model):
    publish_request = models.ForeignKey(PublishRequest, related_name="documents")
    resource_type = models.ForeignKey(OfficialResourceType)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    json_data = JSONField(default=dict)
