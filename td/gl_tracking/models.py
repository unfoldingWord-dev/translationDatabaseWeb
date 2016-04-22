from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.urlresolvers import reverse


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
    words = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @classmethod
    def total_words(cls):
        return sum(cls.objects.filter(is_active=True).values_list("words", flat=True))


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
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Progress, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("language", "type")


# ------------- #
#    PARTNER    #
# ------------- #
@python_2_unicode_compatible
class Partner(models.Model):

    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    province = models.CharField(max_length=200, blank=True)  # This is used for State also
    country = models.ForeignKey("td.Country", on_delete=models.SET_NULL, null=True, blank=True)

    partner_start = models.DateField(blank=True, default=datetime.date(1900, 1, 1))
    partner_end = models.DateField(null=True, blank=True)

    # Contact Information
    contact_name = models.CharField(max_length=200, blank=True)
    contact_phone = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(max_length=200, blank=True)

    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # The "default" arg in DateField() seems to only work for existing record, not new ones.
        # There's need to set initial value in the form after this.
        if self.partner_start is None:
            self.partner_start = datetime.date(1900, 1, 1)
        super(Partner, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("gl:partner_detail_view", kwargs={"pk": self.pk})


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
    regions = models.ManyToManyField("td.WARegion", blank=True)
    is_helper = models.BooleanField(default=False)
    is_super = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @property
    def name(self):
        full_name = " ".join([self.user.first_name, self.user.last_name])
        return full_name if full_name != " " else self.user.username

    @classmethod
    def super_gl_directors(cls):
        return [d.user.username for d in cls.objects.filter(is_super=True)]
