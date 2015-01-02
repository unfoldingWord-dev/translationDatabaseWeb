from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible

from td.imports.models import EthnologueCountryCode
from td.models import Language as SourceLanguage


@python_2_unicode_compatible
class Network(models.Model):
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse("network_detail", args=[self.pk])

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BibleContent(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Country(models.Model):
    country = models.ForeignKey(EthnologueCountryCode)
    population = models.IntegerField(null=True, blank=True)
    primary_networks = models.ManyToManyField(Network, blank=True)

    def __str__(self):
        return self.country.name


@python_2_unicode_compatible
class Language(models.Model):
    country = models.ForeignKey(Country)
    living_language = models.ForeignKey(SourceLanguage, related_name="+")
    gateway_dialect = models.ForeignKey(SourceLanguage, related_name="+", null=True, blank=True)
    native_speakers = models.IntegerField(null=True, blank=True)
    networks_translating = models.ManyToManyField(Network, null=True, blank=True)

    def __str__(self):
        return self.living_language.name


@python_2_unicode_compatible
class Entity(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, blank=True, help_text="Email address.")
    d43username = models.CharField(max_length=255, blank=True, help_text="Door43 username.")
    location = models.CharField(max_length=255, blank=True, help_text="Location.")
    phone = models.CharField(max_length=255, blank=True, help_text="Phone number.")

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Translator(Entity):
    languages = models.ManyToManyField(Language, related_name="Contact", help_text="Langauges spoken by contact.")
    relationship = models.TextField(blank=True, help_text="Relationships to other people or organizations.")
    other = models.CharField(max_length=255, blank=True, help_text="Other information.")


class Organization(Entity):
    pass


class ScriptureBase(models.Model):
    KIND_FULL_BIBLE = "full-bible"
    KIND_FULL_NT = "full-nt"
    KIND_PORTIONS = "portions"
    KIND_AUDIO = "audio"
    KIND_VIDEO = "video"
    KIND_BRAILLE = "braille"
    KIND_CHILDREN = "children"
    KIND_OBS = "obs"
    KIND_CHOICES = [
        (KIND_FULL_BIBLE, "Full Bible"),
        (KIND_FULL_NT, "Full NT"),
        (KIND_PORTIONS, "Bible Portions"),
        (KIND_AUDIO, "Audio"),
        (KIND_VIDEO, "Video"),
        (KIND_BRAILLE, "Braille"),
        (KIND_CHILDREN, "Illustrated Children's"),
        (KIND_OBS, "Open Bible Stories")
    ]
    kind = models.CharField(max_length=50, choices=KIND_CHOICES)
    language = models.ForeignKey(Language)
    bible_content = models.ForeignKey(BibleContent, verbose_name="Bible Content")

    class Meta:
        abstract = True


@python_2_unicode_compatible
class WorkInProgress(ScriptureBase):
    PARADIGM_P1 = "P1"
    PARADIGM_P2 = "P2"
    PARADIGM_P3 = "P3"
    PARADIGM_CHOICES = [
        (PARADIGM_P1, "P1"),
        (PARADIGM_P2, "P2"),
        (PARADIGM_P3, "P3")
    ]
    paradigm = models.CharField(max_length=2, choices=PARADIGM_CHOICES)
    translators = models.ManyToManyField(Translator, blank=True)
    anticipated_completion_date = models.DateField()

    def __str__(self):
        return "{}: {} ({})".format(self.get_kind_display(), self.bible_content.name, self.language.living_language.name)


class Scripture(ScriptureBase):
    wip = models.ForeignKey(WorkInProgress, verbose_name="Work in Progress", null=True, blank=True)
    year = models.IntegerField()
    publisher = models.CharField(max_length=200)


class TranslationNeed(models.Model):
    language = models.ForeignKey(Language)
    text_gaps = models.TextField(blank=True)
    text_updates = models.TextField(blank=True)
    other_gaps = models.TextField(blank=True)
    other_updates = models.TextField(blank=True)


class Resource(models.Model):
    language = models.ForeignKey(Language)
    name = models.CharField(max_length=200)
    copyright = models.CharField(max_length=100, blank=True)
    copyright_holder = models.ForeignKey(Organization, blank=True, null=True)
    license = models.TextField(blank=True)
