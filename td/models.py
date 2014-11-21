from django.db import connection
from django.db import models
from django.utils import timezone

from eventlog.models import log

from td.imports.models import EthnologueCountryCode, EthnologueLanguageCode


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
    def country_code(self):
        if self.country:
            return self.country.code.encode("utf-8")
        return ""

    @property
    def region(self):
        if self.country:
            return self.country.area.encode("utf-8")
        return ""

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
            dict(lc=x.code, ln=x.name.encode("utf-8"), cc=[x.country_code], lr=x.region)
            for x in cls.objects.all().order_by("code")
        ]

    @classmethod
    def integrate_imports(cls):
        additionals = {
            x.two_letter or x.three_letter or x.ietf_tag: x.native_name or x.common_name
            for x in AdditionalLanguage.objects.all()
        }
        cursor = connection.cursor()
        cursor.execute("""
    select coalesce(nullif(x.part_1, ''), x.code) as code,
           coalesce(nullif(nn1.native_name, ''), nullif(nn2.native_name, ''), x.ref_name) as name,
           coalesce(cc.id, -1)
      from imports_ethnologuelanguagecode lc
 left join imports_sil_iso_639_3 x on x.code = lc.code
 left join imports_wikipediaisolanguage nn1 on x.part_1 = nn1.iso_639_1
 left join imports_wikipediaisolanguage nn2 on x.code = nn2.iso_639_3
 left join imports_ethnologuecountrycode cc on lc.country_code = cc.code
     where lc.status = %s order by code;
""", [EthnologueLanguageCode.STATUS_LIVING])
        rows = cursor.fetchall()
        rows.extend([(x[0], x[1], -1) for x in additionals.items()])
        rows.sort()
        rows = [
            cls(
                code=r[0].encode("utf-8"),
                name=r[1].encode("utf-8"),
                country=next(iter(EthnologueCountryCode.objects.filter(pk=int(r[2]))), None)
            )
            for r in rows
            if r[0] is not None
        ]
        cls.objects.all().delete()
        cls.objects.bulk_create(rows)
        log(user=None, action="INTEGRATED_SOURCE_DATA", extra={})
