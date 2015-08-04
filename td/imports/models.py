import csv

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from td.utils import str_to_bool

import bs4
import xlrd

from pinax.eventlog.models import log
from . import fetch


@python_2_unicode_compatible
class WikipediaISOCountry(models.Model):
    english_short_name = models.CharField(max_length=100)
    alpha_2 = models.CharField(max_length=2)
    alpha_3 = models.CharField(max_length=3)
    numeric_code = models.CharField(max_length=3)
    iso_3166_2_code = models.CharField(max_length=20)

    def __str__(self):
        return "{0} ({1}) ({2})".format(self.english_short_name, self.alpha_2, self.alpha_3)

    class Meta:
        verbose_name = "Wikipedia ISO 3166-1 Country"
        verbose_name_plural = "Wikipedia ISO 3166-1 Countries"

    @classmethod
    def reload(cls, session):
        content = fetch.WikipediaCountryFetcher(session).fetch()
        if not content:
            return
        soup = bs4.BeautifulSoup(content)
        records = []
        for tr in soup.select("table.sortable tr"):
            row = [td.text for td in tr.find_all("td")]
            if len(row) == 5:
                records.append(cls(
                    english_short_name=row[0].strip(),
                    alpha_2=row[1].strip(),
                    alpha_3=row[2].strip(),
                    numeric_code=row[3].strip(),
                    iso_3166_2_code=row[4].strip()
                ))
        if len(records) > 0:
            cls.objects.all().delete()
            cls.objects.bulk_create(records)
            log(user=None, action="SOURCE_WIKIPEDIA_COUNTRIES_RELOADED", extra={})


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

    def __str__(self):
        return self.language_name

    def __unicode__(self):
        return self.language_name

    class Meta:
        verbose_name = "Wikipedia ISO Language"

    @classmethod
    def reload(cls, session):
        content = fetch.WikipediaFetcher(session).fetch()
        if not content:
            return
        soup = bs4.BeautifulSoup(content)
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

    SCOPE_INDIVIDUAL = "I"
    SCOPE_MACRO_LANGUAGE = "M"
    SCOPE_SPECIAL = "S"
    SCOPE_CHOICES = [
        (SCOPE_INDIVIDUAL, "Individual"),
        (SCOPE_MACRO_LANGUAGE, "Macrolanguage"),
        (SCOPE_SPECIAL, "Special")
    ]

    TYPE_ANCIENT = "A"
    TYPE_CONSTRUCTED = "C"
    TYPE_EXTINCT = "E"
    TYPE_HISTORICAL = "H"
    TYPE_LIVING = "L"
    TYPE_SPECIAL = "S"
    TYPE_CHOICES = [
        (TYPE_ANCIENT, "Ancient"),
        (TYPE_CONSTRUCTED, "Constructed"),
        (TYPE_EXTINCT, "Extinct"),
        (TYPE_HISTORICAL, "Historical"),
        (TYPE_LIVING, "Living"),
        (TYPE_SPECIAL, "Special")
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

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name = "SIL ISO Code Set"

    @classmethod
    def reload(cls, session):
        content = fetch.ISO_639_3Fetcher(session).fetch()
        if not content:
            return
        reader = csv.DictReader(StringIO(content), dialect="excel-tab")
        rows_updated = rows_created = 0
        for row in reader:
            defaults = dict(
                part_2b=row["Part2B"] or "",
                part_2t=row["Part2T"] or "",
                part_1=row["Part1"] or "",
                scope=row["Scope"],
                language_type=row["Language_Type"],
                ref_name=row["Ref_Name"],
                comment=row["Comment"] or ""
            )
            record, created = cls.objects.get_or_create(
                code=row["Id"],
                defaults=defaults
            )
            if created:
                rows_created += 1
            else:
                for key in defaults:
                    setattr(record, key, defaults[key])
                record.save()
                rows_updated += 1
        log(user=None, action="SOURCE_SIL_ISO_639_3_RELOADED", extra={
            "rows_created": rows_created,
            "rows-updated": rows_updated
        })


class EthnologueLanguageCode(models.Model):

    STATUS_EXTINCT = "E"
    STATUS_LIVING = "L"
    STATUS_CHOICES = [
        (STATUS_EXTINCT, "Extinct"),
        (STATUS_LIVING, "Living"),
    ]

    code = models.CharField(max_length=3, unique=True)
    country_code = models.CharField(max_length=2)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    name = models.CharField(max_length=75)
    date_imported = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name = "Ethnologue Language Code"

    @classmethod
    def reload(cls, session):
        content = fetch.EthnologueLanguageCodesFetcher(session).fetch()
        if not content:
            return
        reader = csv.DictReader(StringIO(content), dialect="excel-tab")
        rows_updated = rows_created = 0
        for row in reader:
            defaults = dict(
                country_code=row["CountryID"],
                status=row["LangStatus"],
                name=row["Name"],
            )
            record, created = cls.objects.get_or_create(
                code=row["LangID"],
                defaults=defaults
            )
            if created:
                rows_created += 1
            else:
                for key in defaults:
                    setattr(record, key, defaults[key])
                record.save()
                rows_updated += 1
        log(user=None, action="SOURCE_ETHNOLOGUE_LANG_CODE_RELOADED", extra={
            "rows_created": rows_created,
            "rows-updated": rows_updated
        })


class EthnologueCountryCode(models.Model):

    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=75)
    area = models.CharField(max_length=10)
    date_imported = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name = "Ethnologue Country Code"

    @classmethod
    def reload(cls, session):
        content = fetch.EthnologueCountryCodesFetcher(session).fetch()
        if not content:
            return
        reader = csv.DictReader(StringIO(content), dialect="excel-tab")
        rows_updated = rows_created = 0
        for row in reader:
            defaults = dict(
                name=row["Name"],
                area=row["Area"]
            )
            record, created = cls.objects.get_or_create(
                code=row["CountryID"],
                defaults=defaults
            )
            if created:
                rows_created += 1
            else:
                for key in defaults:
                    setattr(record, key, defaults[key])
                record.save()
                rows_updated += 1
        log(user=None, action="SOURCE_ETHNOLOGUE_COUNTRY_CODE_RELOADED", extra={
            "rows_created": rows_created,
            "rows-updated": rows_updated
        })


class EthnologueLanguageIndex(models.Model):

    TYPE_LANGUAGE = "L"
    TYPE_LANGUAGE_ALTERNATE = "LA"
    TYPE_DIALECT = "D"
    TYPE_DIALECT_ALTERNATE = "DA"
    TYPE_LANGUAGE_PEJORAATIVE = "LP"
    TYPE_DIALECT_PEJORATIVE = "DP"
    TYPE_CHOICES = [
        (TYPE_LANGUAGE, "Language"),
        (TYPE_LANGUAGE_ALTERNATE, "Language Alternate"),
        (TYPE_DIALECT, "Dialect"),
        (TYPE_DIALECT_ALTERNATE, "Dialect Alternate"),
        (TYPE_LANGUAGE_PEJORAATIVE, "Language Pejorative"),
        (TYPE_DIALECT_PEJORATIVE, "Dialect Pejorative")
    ]

    language_code = models.CharField(max_length=3)
    country_code = models.CharField(max_length=2)
    name_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    name = models.CharField(max_length=75)
    date_imported = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Ethnologue Language Index"
        verbose_name_plural = "Ethnologue Language Index"

    @classmethod
    def reload(cls, session):
        content = fetch.EthnologueLanguageIndexFetcher(session).fetch()
        if not content:
            return
        reader = csv.DictReader(StringIO(content), dialect="excel-tab")
        rows_updated = rows_created = 0
        for row in reader:
            record, created = cls.objects.get_or_create(
                language_code=row["LangID"],
                country_code=row["CountryID"],
                name_type=row["NameType"],
                name=row["Name"]
            )
            if created:
                rows_created += 1
            else:
                rows_updated += 1  # @@@ Should never be an update on this table
        log(user=None, action="SOURCE_ETHNOLOGUE_LANG_INDEX_RELOADED", extra={
            "rows_created": rows_created,
            "rows-updated": rows_updated
        })


@python_2_unicode_compatible
class IMBPeopleGroup(models.Model):
    peid = models.BigIntegerField(primary_key=True, verbose_name="PEID")
    affinity_bloc = models.CharField(max_length=75)
    people_cluster = models.CharField(max_length=75)
    continent = models.CharField(max_length=20)
    sub_continent = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    country_of_origin = models.CharField(max_length=50, blank=True)
    people_group = models.CharField(max_length=50, db_index=True)
    global_status_evangelical_christianity = models.IntegerField(default=0)
    evangelical_engagement = models.BooleanField(default=False)
    population = models.BigIntegerField(default=0)
    dispersed = models.NullBooleanField(blank=True, null=True, default=None)
    rol = models.CharField(max_length=3, db_index=True, verbose_name="ROL")
    language = models.CharField(max_length=75)
    religion = models.CharField(max_length=75)
    written_scripture = models.BooleanField(default=False)
    jesus_film = models.BooleanField(default=False)
    radio_broadcast = models.BooleanField(default=False)
    gospel_recording = models.BooleanField(default=False)
    audio_scripture = models.BooleanField(default=False)
    bible_stories = models.BooleanField(default=False)
    resources = models.IntegerField(default=0)
    physical_exertion = models.CharField(max_length=20)
    freedom_index = models.CharField(max_length=20)
    government_restrictions_index = models.CharField(max_length=20)
    social_hostilities_index = models.CharField(max_length=20)
    threat_level = models.CharField(max_length=20)
    prayer_threads = models.NullBooleanField(default=None, blank=True)
    sbc_embracing_relationship = models.NullBooleanField(default=None, blank=True, null=True)
    embracing_priority = models.BooleanField(default=False)
    rop1 = models.CharField(max_length=4, verbose_name="ROP1")
    rop2 = models.CharField(max_length=5, verbose_name="ROP2")
    rop3 = models.DecimalField(max_digits=6, decimal_places=0, verbose_name="ROP3")
    people_name = models.CharField(max_length=75)
    fips = models.CharField(max_length=2, verbose_name="FIPS")
    fips_of_origin = models.CharField(max_length=2, default="", blank=True, verbose_name="FIPS of Origin")
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    peid_of_origin = models.BigIntegerField(default=0, blank=0, verbose_name="PEID of Origin")
    imb_affinity_group = models.CharField(max_length=75, verbose_name="IMB Affinity Group")

    def __str__(self):
        return "%s (%s)" % (self.people_group, str(self.peid))

    class Meta:
        verbose_name = "IMB People Group"
        verbose_name_plural = "IMB People Groups"

    @classmethod
    def reload(cls, session):
        content = fetch.IMBPeopleFetcher(session).fetch()
        if content is None or content == "":
            return
        book = xlrd.open_workbook(file_contents=content)
        sheet = book.sheet_by_index(0)
        key_cell = (4, 0)   # todo: replace this with code to "find" the PEID column properly
        sh_field_names = [sheet.cell_value(key_cell[0], key_cell[1] + x) for x in range(0, 40)]
        current_row_num = key_cell[0] + 1
        rows_created = rows_updated = 0
        while True:
            row = {sh_field_names[x]: sheet.cell_value(current_row_num, x) for x in range(0, 40)}
            if str(row["PEID"]) == "":
                break
            defaults = dict(
                affinity_bloc=row["Affinity Bloc"],
                people_cluster=row["People Cluster"],
                continent=row["Continent"],
                sub_continent=row["Sub-Continent"],
                country=row["Country"],
                country_of_origin=row["Country of Origin"],
                people_group=row["People Group"],
                global_status_evangelical_christianity=row["Global Status of  Evangelical Christianity"],
                evangelical_engagement=str_to_bool(row["Evangelical Engagement"]),
                population=row["Population"],
                dispersed=str_to_bool(row["Dispersed (Yes/No)"], allow_null=True),
                rol=row["ROL"],
                language=row["Language"],
                religion=row["Religion"],
                written_scripture=str_to_bool(row["Written Scripture"]),
                jesus_film=str_to_bool(row["Jesus Film"]),
                radio_broadcast=str_to_bool(row["Radio Broadcast"]),
                gospel_recording=str_to_bool(row["Gospel Recording"]),
                audio_scripture=str_to_bool(row["Audio Scripture"]),
                bible_stories=str_to_bool(row["Bible Stories"]),
                resources=row["Resources"],
                physical_exertion=row["Physical Exertion"],
                freedom_index=row["Freedom Index"],
                government_restrictions_index=row["Government Restrictions Index"],
                social_hostilities_index=row["Social Hostilities Index"],
                threat_level=row["Threat Level"],
                prayer_threads=str_to_bool(row["Prayer Threads"], allow_null=True),
                sbc_embracing_relationship=str_to_bool(row["SBC Embracing Relationship"], allow_null=True),
                embracing_priority=str_to_bool(row["Embracing Priority"]),
                rop1=row["ROP1"],
                rop2=row["ROP2"],
                rop3=row["ROP3"],
                people_name=row["People Name"],
                fips=row["FIPS"],
                fips_of_origin=row["FIPS of Origin"],
                latitude=row["Latitude"],
                longitude=row["Longitude"],
                peid_of_origin=row["PEID of Origin"],
                imb_affinity_group=row["IMB Affinity Group"]
            )
            record, created = cls.objects.get_or_create(
                peid=row["PEID"],
                defaults=defaults
            )
            if created:
                rows_created += 1
            else:
                for key in defaults:
                    setattr(record, key, defaults[key])
                record.save()
                rows_updated += 1
            current_row_num += 1
        log(user=None, action="SOURCE_IMB_PEOPLE_GROUPS_LOADED", extra={
            "rows_created": rows_created,
            "rows-updated": rows_updated
        })
