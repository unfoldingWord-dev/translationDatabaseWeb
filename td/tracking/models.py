from django.db import models
from django.utils import timezone

from td.models import Language, Country, Network


# Choices

DUMMY_CHOICES = {
    ('1', '1'),
    ('2', '2')
}

TRANSLATION_METHODOLOGIES_CHOICES = (
    ('church', 'Church group'),
    ('door43web', 'Door43 Website'),
    ('mast', 'MAST'),
    ('seedco', 'Seed Co.'),
    ('sovee-memoq', 'Sovee/MemoQ'),
    ('translator', 'Translator'),
    ('ts', 'translationStudio'),
    ('other', 'Other'),
)

SOFTWARE_CHOICES = (
    ('door43web', 'Door43 Website'),
    ('msword', 'Microsoft Word'),
    ('paratext', 'ParaText'),
    ('sovee-memoq', 'Sovee/MemoQ'),
    ('ts', 'translationStudio'),
    ('other', 'Other'),
)

EQUIPMENT_CHOICES = (
    ('tablet', 'Tablet'),
    ('laptop', 'Laptop'),
    ('keyboard-layout', 'Keyboard Layout'),
    ('fonts', 'Fonts'),
    ('word-template', 'Word Template'),
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
    )

    start_date = models.DateField(
        verbose_name="Start Date",
    )

    end_date = models.DateField(
        verbose_name="Projected Completion Date",
    )

    lead_dept = models.ForeignKey(
        'Department',
        verbose_name="Lead Department",
        related_name='event_lead_dept',
    )

    output_target = models.TextField(
        max_length=1500,
        blank=True,
    )

    translation_method = models.SlugField(
        choices=TRANSLATION_METHODOLOGIES_CHOICES,
        blank=True,
    )

    tech_used = models.SlugField(
        choices=SOFTWARE_CHOICES,
        blank=True,
    )

    comp_tech_used = models.SlugField(
        choices=EQUIPMENT_CHOICES,
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
    materials = models.ManyToManyField(
        'Material'
    )
    translators = models.ManyToManyField(
        'Translator'
    )
    facilitators = models.ManyToManyField(
        'Facilitator'
    )
    networks = models.ManyToManyField(
        Network,
    )
    departments = models.ManyToManyField(
        'Department',
        help_text='Supporting Departments',
        related_name='event_supporting_dept'
    )

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


class Department(models.Model):

    name = models.CharField(
        max_length=200
    )

    def __unicode__(self):
        return self.name
