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
        soup = bs4.BeautifulSoup(response.text)
        records = []
        for tr in soup.select("table.wikitable tr"):
            row = [td.text for td in tr.find_all("td")]
            if len(row) == 10:
                records.append(cls(
                    language_family=row[1],
                    language_name=row[2],
                    native_name=row[3],
                    iso_639_1=row[4][:2],
                    iso_639_2t=row[5][:3],
                    iso_639_2b=row[6][:3],
                    iso_639_3=row[7][:3],
                    iso_639_9=row[8][:4],
                    notes=row[9]
                ))
        if len(records) > 0:
            cls.objects.all().delete()
            cls.objects.bulk_create(records)
            log(user=None, action="SOURCE_WIKIPEDIA_RELOADED", extra={})
