from django.db import models
from django.utils import timezone

from td.imports.models import EthnologueCountryCode


class AdditionalLanguage(models.Model):

    ietf_tag = models.CharField(max_length=100)
    common_name = models.CharField(max_length=100)
    two_letter = models.CharField(max_length=2, blank=True)
    three_letter = models.CharField(max_length=3, blank=True)
    native_name = models.CharField(max_length=100, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super(AdditionalLanguage, self).save(*args, **kwargs)

    def __str__(self):
        return self.ietf_tag

    def __unicode__(self):
        return self.ietf_tag

    class Meta:
        verbose_name = "Additional Language"


class Language(models.Model):

    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(EthnologueCountryCode, blank=True, null=True)

    def __unicode__(self):
        return self.name

    @property
    def cc(self):
        if self.country:
            return self.country.code.encode("utf-8")
        return ""

    @property
    def lr(self):
        if self.country:
            return self.country.area.encode("utf-8")
        return ""

    @property
    def lc(self):
        return self.code

    @property
    def ln(self):
        return self.name.encode("utf-8")

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
    def names_data(cls):
        return [
            dict(lc=x.lc, ln=x.ln, cc=[x.cc], lr=x.lr)
            for x in cls.objects.all().order_by("code")
        ]
