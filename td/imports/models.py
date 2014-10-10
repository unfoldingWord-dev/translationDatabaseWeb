import csv

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from django.db import models
from django.utils import timezone

import bs4
import requests

from eventlog.models import log


class WikipediaISOLanguage(models.Model):

    language_family = models.CharField(max_length=100)
    language_name = models.CharField(max_length=100)
    native_name = models.CharField(max_length=100)
    iso_639_1 = models.CharField(max_length=2)
    iso_639_2t = models.CharField(max_length=3, blank=True)
    iso_639_2b = models.CharField(max_length=3, blank=True)
    iso_639_3 = models.CharField(max_length=3, blank=True)
    iso_639_9 = models.CharField(max_length=4, blank=True)
    notes = models.TextField(blank=True)
    date_imported = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.language_name

    class Meta:
        verbose_name = "Wikipedia ISO Language"

    @classmethod
    def reload(cls):
        response = requests.get("http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes")
        if response.status_code != 200:
            log(
                user=None,
                action="SOURCE_WIKIPEDIA_RELOAD_FAILED",
                extra={"status_code": response.status_code, "text": response.content}
            )
            return
        soup = bs4.BeautifulSoup(response.content)
        records = []
        for tr in soup.select("table.wikitable tr"):
            row = [td.text for td in tr.find_all("td")]
            if len(row) == 10:
                records.append(cls(
                    language_family=row[1].strip(),
                    language_name=row[2].strip(),
                    native_name=row[3].strip(),
                    iso_639_1=row[4][:2].strip(),
                    iso_639_2t=row[5][:3].strip(),
                    iso_639_2b=row[6][:3].strip(),
                    iso_639_3=row[7][:3].strip(),
                    iso_639_9=row[8][:4].strip(),
                    notes=row[9].strip()
                ))
        if len(records) > 0:
            cls.objects.all().delete()
            cls.objects.bulk_create(records)
            log(user=None, action="SOURCE_WIKIPEDIA_RELOADED", extra={})


class SIL_ISO_639_3(models.Model):

    SCOPE_CHOICES = [
        ("I", "Individual"),
        ("M", "Macrolanguage"),
        ("S", "Special")
    ]
    TYPE_CHOICES = [
        ("A", "Ancient"),
        ("C", "Constructed"),
        ("E", "Extinct"),
        ("H", "Historical"),
        ("L", "Living"),
        ("S", "Special")
    ]

    code = models.CharField(max_length=3)
    part_2b = models.CharField(max_length=3, blank=True)
    part_2t = models.CharField(max_length=3, blank=True)
    part_1 = models.CharField(max_length=2, blank=True)
    scope = models.CharField(max_length=1, choices=SCOPE_CHOICES)
    language_type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    ref_name = models.CharField(max_length=150)
    comment = models.CharField(max_length=150, blank=True)
    date_imported = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name = "SIL ISO Code Set"

    @classmethod
    def reload(cls):
        response = requests.get("http://www-01.sil.org/iso639-3/iso-639-3.tab")
        if response.status_code != 200:
            log(
                user=None,
                action="SOURCE_SIL_ISO_639_3_RELOAD_FAILED",
                extra={"status_code": response.status_code, "text": response.content}
            )
            return
        reader = csv.DictReader(StringIO(response.content), dialect="excel-tab")
        records = []
        for row in reader:
            records.append(cls(
                code=row["Id"],
                part_2b=row["Part2B"] or "",
                part_2t=row["Part2T"] or "",
                part_1=row["Part1"] or "",
                scope=row["Scope"],
                language_type=row["Language_Type"],
                ref_name=row["Ref_Name"],
                comment=row["Comment"] or ""
            ))
        if len(records) > 0:
            cls.objects.all().delete()
            cls.objects.bulk_create(records)
            log(user=None, action="SOURCE_SIL_ISO_639_3_RELOADED", extra={})
