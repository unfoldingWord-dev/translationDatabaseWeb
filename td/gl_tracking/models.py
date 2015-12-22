from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils import timezone

# from td.models import Language


# ------------- #
#    CHOICES    #
# ------------- #
METHODS = (
    ('online', 'Online'),
    ('offline', 'Offline'),
    ('mast', 'MAST'),
    ('d43', 'door43'),
    ('ts', 'translationStudio'),
    ('memoq', 'MemoQ'),
    ('sovee', 'Sovee'),
)

COMPLETION_RATE = (
    (2, '2%'),
    (25, '25%'),
    (50, '50%'),
    (75, '75%'),
    (99, '99%'),
    (100, '100%'),
)

QA_LEVEL = (
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
)


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
    code = models.SlugField(max_length=4, unique=True, default='')
    description = models.TextField(blank=True)
    category = models.ForeignKey('DocumentCategory', null=True)

    def __str__(self):
        return self.name


# -------------- #
#    PROGRESS    #
# -------------- #
@python_2_unicode_compatible
class Progress(models.Model):

    language = models.ForeignKey('td.Language', limit_choices_to={'gateway_flag': True})
    type = models.ForeignKey('Document')
    is_online = models.NullBooleanField()
    method = models.CharField(max_length=200, choices=METHODS, blank=True)
    completion_rate = models.PositiveSmallIntegerField(choices=COMPLETION_RATE, null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    qa_level = models.PositiveSmallIntegerField(choices=QA_LEVEL, null=True, blank=True)
    in_door43 = models.NullBooleanField()
    in_uw = models.NullBooleanField()
    partners = models.ManyToManyField('Partner', blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return str(self.type)

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
