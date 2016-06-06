from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from collections import defaultdict

from jsonfield import JSONField
from model_utils import FieldTracker

from td.commenting.models import CommentableModel
from .gl_tracking.models import Document


DIRECTION_CHOICES = (
    ("l", "ltr"),
    ("r", "rtl")
)


@python_2_unicode_compatible
class JSONData(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.SlugField(max_length=50)
    data = JSONField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TempLanguage(models.Model):
    APP_CHOICES = (
        ("td", "translationDatabase"),
        ("ts-android", "translationStudio Android"),
        ("ts-desktop", "translationStudio Desktop"),
        ("tr", "translationRecorder"),
    )
    STATUS_CHOICES = (
        ("p", "Pending"),
        ("a", "Approved"),
        ("r", "Rejected"),
    )
    code = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=200, blank=True)
    country = models.ForeignKey("Country", on_delete=models.SET_NULL, null=True)
    direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES, default="l")
    app = models.CharField(max_length=10, choices=APP_CHOICES, blank=True)
    requester = models.CharField(max_length=100)
    questionnaire = models.ForeignKey("resources.Questionnaire", on_delete=models.PROTECT, null=True)
    answers = JSONField(blank=True)
    request_id = models.SlugField(max_length=50, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="p")
    status_comment = models.TextField(blank=True)
    lang_assigned = models.OneToOneField("Language", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="templanguage_created", null=True,
                                   blank=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="templanguage_modified", null=True,
                                    blank=True, editable=False)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('templanguage_detail', args=[str(self.id)])

    @property
    def lang_assigned_url(self):
        return reverse('language_detail', args=[str(self.lang_assigned_id)]) if self.lang_assigned_id else ""

    @property
    def questions_and_answers(self):
        answers = {}
        if self.answers is not None:
            for a in self.answers:
                answers[str(a["question_id"])] = a["text"]
        questions = []
        # Build a list of questions
        for q in self.questionnaire.questions:
            if str(q["id"]) in answers:
                question_answer = answers[str(q["id"])]
            else:
                question_answer = ""
            questions.append({"id": q["id"], "question": q["text"], "answer": question_answer})
        # Now match in the answers
        return questions

    @classmethod
    def pending(cls):
        return cls.objects.filter(status="p")

    @classmethod
    def approved(cls):
        return cls.objects.filter(status="a")

    @classmethod
    def rejected(cls):
        return cls.objects.filter(status="r")

    @classmethod
    def lang_assigned_data(cls):
        return [{"pk": x.pk, "lc": x.code, "ln": x.name, "ang": x.lang_assigned.ang, "alt": x.lang_assigned.alt_name_all,
                 "cc": [x.country.code] if x.country is not None else [], "lr": x.lang_assigned.lr,
                 "gw": x.lang_assigned.gateway_flag, "ld": x.get_direction_display()} for x in cls.objects.all()]

    @classmethod
    def lang_assigned_map(cls):
        return [{x.code: x.lang_assigned.lc} for x in cls.objects.all() if x.lang_assigned is not None]

    @classmethod
    def lang_assigned_changed_map(cls):
        return [{x.code: x.lang_assigned.lc}
                for x in cls.objects.all() if x.lang_assigned is not None and x.code != x.lang_assigned.lc]


@python_2_unicode_compatible
class AdditionalLanguage(models.Model):
    ietf_tag = models.CharField(max_length=100)
    common_name = models.CharField(max_length=100)
    two_letter = models.CharField(max_length=2, blank=True)
    three_letter = models.CharField(max_length=3, blank=True)
    native_name = models.CharField(max_length=100, blank=True)
    direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES, default="l")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def merge_code(self):
        return self.two_letter or self.three_letter or self.ietf_tag

    def merge_name(self):
        return self.native_name or self.common_name

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super(AdditionalLanguage, self).save(*args, **kwargs)

    def __str__(self):
        return self.ietf_tag

    class Meta:
        verbose_name = "Additional Language"


@python_2_unicode_compatible
class Network(models.Model):
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse("network_detail", args=[self.pk])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'uw_network'


@python_2_unicode_compatible
class Region(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    tracker = FieldTracker()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'uw_region'
        ordering = ['name']


@python_2_unicode_compatible
class WARegion(CommentableModel):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    tracker = FieldTracker()

    class Meta:
        db_table = 'wa_region'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("wa_region_detail", kwargs={"slug": self.slug})

    @property
    def gl_directors(self):
        return [d.name for d in self.gldirector_set.filter(is_helper=False)]

    @property
    def gl_helpers(self):
        return [d.name for d in self.gldirector_set.filter(is_helper=True)]

    @property
    def tag_slug(self):
        return self.slug

    @property
    def tag_tip(self):
        return ""

    @classmethod
    def slug_all(cls):
        return [r.slug for r in cls.objects.all()]


@python_2_unicode_compatible
class Country(CommentableModel):
    code = models.CharField(max_length=2, unique=True)
    alpha_3_code = models.CharField(max_length=3, blank=True, default="")
    name = models.CharField(max_length=75)
    region = models.ForeignKey(Region, null=True, blank=True, related_name="countries")
    wa_region = models.ForeignKey(WARegion, null=True, blank=True, on_delete=models.SET_NULL)
    population = models.IntegerField(null=True, blank=True)
    primary_networks = models.ManyToManyField(Network, blank=True, db_table='uw_country_primary_networks')
    extra_data = JSONField(default=dict)

    tracker = FieldTracker()

    class Meta:
        db_table = 'uw_country'

    def gateway_language(self):
        if not hasattr(self, "_gateway_language"):
            data = self.extra_data
            if not isinstance(data, dict):
                data = {}
            self._gateway_language = next(iter(Language.objects.filter(code=data.get("gateway_language"))), None)
        return self._gateway_language

    def gateway_languages(self, with_primary=True):
        gl = self.gateway_language()
        if gl:
            ogls = [gl]
        else:
            ogls = []
        for lang in self.language_set.all():
            if lang.gateway_flag and lang not in ogls:
                ogls.append(lang)
            elif lang.gateway_language and lang.gateway_language not in ogls:
                ogls.append(lang.gateway_language)
        if not with_primary and gl:
            ogls.remove(gl)
        return ogls

    @classmethod
    def regions(cls):
        qs = cls.objects.all().values_list("region", flat=True).distinct()
        qs = qs.order_by("region.name")
        return qs

    @classmethod
    def gateway_data(cls):
        with_gateways = cls.objects.filter(language__gateway_language__isnull=False).distinct()
        without_gateways = cls.objects.exclude(pk__in=with_gateways)
        data = {
            x.code: {"obj": x, "gateways": defaultdict(lambda: [])}
            for x in with_gateways
        }
        data.update({
            x.code: {"obj": x, "gateways": {"n/a": list(x.language_set.all())}}
            for x in without_gateways
        })
        for country in with_gateways:
            for lang in country.language_set.all():
                if lang.gateway_language:
                    data[country.code]["gateways"][lang.gateway_language.code].append(lang)
                else:
                    data[country.code]["gateways"]["n/a"].append(lang)
        return data

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("country_detail", kwargs={"pk": self.pk})


@python_2_unicode_compatible
class LanguageAltName(models.Model):
    code = models.SlugField(max_length=50, db_index=True)
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        unique_together = ("code", "name")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Language(CommentableModel):
    DIRECTION_CHOICES = (
        ("l", "ltr"),
        ("r", "rtl")
    )

    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, blank=True)
    anglicized_name = models.CharField(max_length=100, blank=True)
    # alt_name is used to link Language to LanguageAltName one-by-one during
    #    import. If there are multiple LanguageAltName, alt_name will be the
    #    lastest linked LanguageAltName by default.
    alt_name = models.ForeignKey(LanguageAltName, null=True, blank=True, on_delete=models.SET_NULL)
    # alt_names is programatically set to be the names of all LangAltName
    #    objects linked to this language. It is modified whenever the
    #    language instance is saved.
    alt_names = models.TextField(editable=False, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    gateway_language = models.ForeignKey("self", related_name="gateway_to", null=True, blank=True)
    native_speakers = models.IntegerField(null=True, blank=True)
    networks_translating = models.ManyToManyField(Network, blank=True, db_table='uw_language_networks_translating')
    gateway_flag = models.BooleanField(default=False, blank=True, db_index=True)
    direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES, default="l")
    iso_639_3 = models.CharField(max_length=3, default="", db_index=True, blank=True, verbose_name="ISO-639-3")
    variant_of = models.ForeignKey("self", related_name="variants", null=True, blank=True)
    wa_region = models.ForeignKey(WARegion, null=True, blank=True)
    extra_data = JSONField(default=dict)
    tracker = FieldTracker()

    class Meta:
        db_table = 'uw_language'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("language_detail", kwargs={"pk": self.pk})

    @property
    def cc(self):
        if self.country:
            return self.country.code.encode("utf-8")
        return ""

    @property
    def cc_all(self):
        pks = [int(pk)
               for pk in self.attributes.filter(attribute="country_id")
                                        .values_list("value", flat=True)]
        countries = Country.objects.filter(pk__in=pks)
        return [c.code.encode("utf-8") for c in countries]

    @property
    def lr(self):
        return self.country.region.name.encode("utf-8") if self.country and self.country.region else ""

    @property
    def lc(self):
        return self.code

    @property
    def ln(self):
        return self.name.encode("utf-8")

    @property
    def ang(self):
        return self.anglicized_name

    @property
    def progress_phase_1(self):
        return self.get_progress("1")

    @property
    def progress_phase_2(self):
        return self.get_progress("2")

    @property
    def documents_phase_1(self):
        return self.get_documents("1")

    @property
    def documents_phase_2(self):
        return self.get_documents("2")

    @property
    def documents_ordered(self):
        return self.progress_set.order_by("type__category__phase__number")

    @property
    def variant_codes(self):
        return [lang.code for lang in self.variants.all()]

    @property
    def alt_name_all(self):
        pks = [int(pk)
               for pk in self.attributes.filter(attribute="alt_name_id")
                                        .values_list("value", flat=True)]
        alt_names = LanguageAltName.objects.filter(pk__in=pks)
        return [n.name.encode("utf-8") for n in alt_names]

    @property
    def tag_display(self):
        return self.anglicized_name or self.name

    @property
    def tag_tip(self):
        return ", ".join(self.alt_name_all).decode("utf-8")

    @property
    def tag_slug(self):
        return self.code.lower() if len(self.code) > 2 else self.iso_639_3.lower()

    def get_progress(self, phase):
        words = 0.0
        total_words = Document.total_words()
        for progress in self.get_documents(phase):
            word_count = progress.type.words
            if type(progress.completion_rate) == int:
                words += (float(progress.completion_rate) / 100 * word_count)
        return round((words / total_words) * 100, 2) if total_words != 0 else 0.0

    def get_documents(self, phase):
        return self.progress_set.filter(type__category__phase__number=str(phase))

    @classmethod
    def codes_text(cls):
        return " ".join([
            x.code
            for x in cls.objects.all().order_by("code")
        ])

    @classmethod
    def names_text(cls):
        return "\n".join([
            "{}\t{}".format(x.code, x.name.encode("utf-8"))
            for x in cls.objects.all().order_by("code")
        ])

    @classmethod
    def names_data(cls, short=False):
        languages = cls.objects.all().order_by("code")
        if short:
            data = [dict(pk=x.pk, lc=x.lc, ln=x.ln, ang=x.ang, lr=x.lr) for x in languages]
        else:
            # Filter out languages that have pending or rejected temporary language
            # NOTE: Can this be simplified or turned into a list comprehension?
            data = []
            for lang in languages:
                try:
                    x = lang if lang.templanguage.status == "a" else None
                except TempLanguage.DoesNotExist:
                    x = lang
                if x:
                    data.append(dict(pk=x.pk, lc=x.lc, ln=x.ln, ang=x.ang, alt=x.alt_name_all, cc=x.cc_all, lr=x.lr,
                                gw=x.gateway_flag, ld=x.get_direction_display()))
        return data


class EAVBase(models.Model):
    attribute = models.CharField(max_length=100)
    value = models.CharField(max_length=250)
    source_ct = models.ForeignKey(ContentType)
    source_id = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class CountryEAV(EAVBase):
    entity = models.ForeignKey(Country, related_name="attributes")

    def __str__(self):
        return self.attribute

    class Meta:
        db_table = 'uw_countryeav'


@python_2_unicode_compatible
class LanguageEAV(EAVBase):
    entity = models.ForeignKey(Language, related_name="attributes")

    def __str__(self):
        return self.attribute

    class Meta:
        db_table = 'uw_languageeav'
