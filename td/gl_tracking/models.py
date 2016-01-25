from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.db import models


# ----------- #
#    PHASE    #
# ----------- #
@python_2_unicode_compatible
class Phase(models.Model):

    number = models.SlugField(unique=True)
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name or "BT Phase " + str(self.number)

    class Meta:
        verbose_name = "Bible Translation Phase"


# ----------------------- #
#    DOCUMENT CATEGORY    #
# ----------------------- #
@python_2_unicode_compatible
class DocumentCategory(models.Model):

    name = models.CharField(max_length=200, unique=True)
    phase = models.ForeignKey('Phase')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Document Category"
        verbose_name_plural = "Document Categories"


# -------------- #
#    DOCUMENT    #
# -------------- #
@python_2_unicode_compatible
class Document(models.Model):

    name = models.CharField(max_length=200, unique=True)
    code = models.SlugField(max_length=10, unique=True, default='')
    description = models.TextField(blank=True)
    category = models.ForeignKey('DocumentCategory', null=True)

    def __str__(self):
        return self.name


# -------------- #
#    PROGRESS    #
# -------------- #
@python_2_unicode_compatible
class Progress(models.Model):
    COMPLETION_RATE = (
        (2, '2%'),
        (25, '25%'),
        (50, '50%'),
        (75, '75%'),
        (99, '99%'),
        (100, '100%'),
    )
    QA_LEVEL = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
    )

    language = models.ForeignKey('td.Language', limit_choices_to={'gateway_flag': True})
    type = models.ForeignKey('Document')
    is_online = models.NullBooleanField(verbose_name="Is Online?")
    methods = models.ManyToManyField('Method', blank=True)
    completion_rate = models.PositiveSmallIntegerField(choices=COMPLETION_RATE, null=True, blank=True, verbose_name="Completion Rate")
    completion_date = models.DateField(null=True, blank=True, verbose_name="Completion Date")
    qa_level = models.PositiveSmallIntegerField(choices=QA_LEVEL, null=True, blank=True, verbose_name="QA Level")
    in_door43 = models.NullBooleanField(verbose_name="Available in Door43.org?")
    in_uw = models.NullBooleanField(verbose_name="Available in UnfoldingWord.org?")
    partners = models.ManyToManyField('Partner', blank=True)
    notes = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False, null=True, default=None)
    created_by = models.ForeignKey(User, related_name="created_by", null=True, blank=True, default=None)
    modified_at = models.DateTimeField(null=True, default=None)
    modified_by = models.ForeignKey(User, related_name="modified_by", null=True, blank=True, default=None)

    def __str__(self):
        return str(self.type)

    def save(self, *args, **kwargs):
        """ Update Timestamp on save """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Progress, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("language", "type")


# ------------- #
#    PARTNER    #
# ------------- #
@python_2_unicode_compatible
class Partner(models.Model):

    name = models.CharField(max_length=200, unique=True)
    is_pseudo = models.BooleanField(default=False)
    contact_person = models.CharField(max_length=200, blank=True)
    contact_number = models.CharField(max_length=200, blank=True)
    contact_person = models.EmailField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    province = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


# ------------ #
#    METHOD    #
# ------------ #
@python_2_unicode_compatible
class Method(models.Model):

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class GLDirector(models.Model):

    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    regions = models.ManyToManyField("td.Region", blank=True)

    def __str__(self):
        return self.user.username
