from django.db import models
from django.utils import timezone

from td.models import Language, Country


# Choices
OUTPUT_TARGETS = (
    ('print', 'print'),
    ('audio', 'audio'),
    ('other', 'other'),
)

TRANSLATION_METHODS = (
    ('lit', 'literal'),
    ('dyn', 'dynamic'),
    ('other', 'other'),
)

TECHNOLOGIES = (
    ('btak', 'btak'),
    ('tk', 'trasnlation keyboard'),
    ('other', 'other'),
)

# Models

class Charter(models.Model):

    language = models.OneToOneField(
        Language,
        unique=True,
        verbose_name='Target Language',
    )
    countries = models.ManyToManyField(
        Country,
        verbose_name="Countries that speak this language",
        help_text="Hold Ctrl while clicking to select multiple countries",
    )

    start_date = models.DateField(
        verbose_name="Start Date",
    )
    end_date = models.DateField(
        verbose_name="Projected Completion Date",
    )

    number = models.CharField(
        max_length=10,
        verbose_name="Project Accounting Number",
    )

    lead_dept = models.ForeignKey(
        'Department',
        verbose_name="Lead Department",
    )
    contact_person = models.CharField(
        max_length=200,
        verbose_name="Follow-up Person",
    )

    created_at = models.DateTimeField(
        default=timezone.now,
    )
    created_by = models.CharField(
        max_length=200,
    )

    def __unicode__(self):
        # Returning the language.name cause encoding error in admin
        return str(self.language.code)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Charter._meta.fields]


class Event(models.Model):

    # Primary key is default

    charter = models.ForeignKey(Charter)

    location = models.CharField(
        max_length=200,
        blank=True,
    )

    start_date = models.DateField(
    )
    end_date = models.DateField(
        blank=True,
    )

    lead_dept = models.CharField(
        max_length=200,
        blank=True,
    )

    output_target = models.SlugField(
        choices=OUTPUT_TARGETS,
        blank=True,
    )

    translation_method = models.SlugField(
        choices=TRANSLATION_METHODS,
        blank=True,
    )

    tech_used = models.SlugField(
        choices=TECHNOLOGIES,
        blank=True,
    )
    comp_tech_used = models.SlugField(
        choices=TECHNOLOGIES,
        blank=True,
    )

    pub_process = models.TextField(
        max_length=1500,
        blank=True,
    )

    follow_up = models.CharField(
        max_length=200,
        blank=True,
    )

    # Relationship fields
    materials = models.ManyToManyField('Material')
    translators = models.ManyToManyField('Translator')
    facilitators = models.ManyToManyField('Facilitator')
    networks = models.ManyToManyField('Network')
    departments = models.ManyToManyField('Department')

    # Functions
    def __unicode__(self):
        return str(self.id)
    
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Event._meta.fields]


class Material(models.Model):

    name = models.CharField(
        max_length=200
    )

    licensed = models.BooleanField(
        default=False
    )


class Translator(models.Model):

    name = models.CharField(
        max_length=200
    )


class Facilitator(models.Model):

    name = models.CharField(
        max_length=200
    )

    is_lead = models.BooleanField(
        default=False
    )

    speaks_gl = models.BooleanField(
        default=False
    )


class Network(models.Model):

    name = models.CharField(
        max_length=200
    )


class Department(models.Model):

    name = models.CharField(
        max_length=200
    )

    def __unicode__(self):
        return self.name