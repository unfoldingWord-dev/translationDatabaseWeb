# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EthnologueCountryCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=2)),
                ('name', models.CharField(max_length=75)),
                ('area', models.CharField(max_length=10)),
                ('date_imported', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Ethnologue Country Code',
            },
        ),
        migrations.CreateModel(
            name='EthnologueLanguageCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=3)),
                ('country_code', models.CharField(max_length=2)),
                ('status', models.CharField(max_length=1, choices=[(b'E', b'Extinct'), (b'L', b'Living')])),
                ('name', models.CharField(max_length=75)),
                ('date_imported', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Ethnologue Language Code',
            },
        ),
        migrations.CreateModel(
            name='EthnologueLanguageIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=3)),
                ('country_code', models.CharField(max_length=2)),
                ('name_type', models.CharField(max_length=2, choices=[(b'L', b'Language'), (b'LA', b'Language Alternate'), (b'D', b'Dialect'), (b'DA', b'Dialect Alternate'), (b'LP', b'Language Pejorative'), (b'DP', b'Dialect Pejorative')])),
                ('name', models.CharField(max_length=75)),
                ('date_imported', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Ethnologue Language Index',
                'verbose_name_plural': 'Ethnologue Language Index',
            },
        ),
        migrations.CreateModel(
            name='IMBPeopleGroup',
            fields=[
                ('peid', models.BigIntegerField(serialize=False, verbose_name=b'PEID', primary_key=True)),
                ('affinity_bloc', models.CharField(max_length=75)),
                ('people_cluster', models.CharField(max_length=75)),
                ('continent', models.CharField(max_length=20)),
                ('sub_continent', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('country_of_origin', models.CharField(max_length=50, blank=True)),
                ('people_group', models.CharField(max_length=50, db_index=True)),
                ('global_status_evangelical_christianity', models.IntegerField(default=0)),
                ('evangelical_engagement', models.BooleanField(default=False)),
                ('population', models.BigIntegerField(default=0)),
                ('dispersed', models.NullBooleanField(default=None)),
                ('rol', models.CharField(max_length=3, verbose_name=b'ROL', db_index=True)),
                ('language', models.CharField(max_length=75)),
                ('religion', models.CharField(max_length=75)),
                ('written_scripture', models.BooleanField(default=False)),
                ('jesus_film', models.BooleanField(default=False)),
                ('radio_broadcast', models.BooleanField(default=False)),
                ('gospel_recording', models.BooleanField(default=False)),
                ('audio_scripture', models.BooleanField(default=False)),
                ('bible_stories', models.BooleanField(default=False)),
                ('resources', models.IntegerField(default=0)),
                ('physical_exertion', models.CharField(max_length=20)),
                ('freedom_index', models.CharField(max_length=20)),
                ('government_restrictions_index', models.CharField(max_length=20)),
                ('social_hostilities_index', models.CharField(max_length=20)),
                ('threat_level', models.CharField(max_length=20)),
                ('prayer_threads', models.NullBooleanField(default=None)),
                ('sbc_embracing_relationship', models.NullBooleanField(default=None)),
                ('embracing_priority', models.BooleanField(default=False)),
                ('rop1', models.CharField(max_length=4, verbose_name=b'ROP1')),
                ('rop2', models.CharField(max_length=5, verbose_name=b'ROP2')),
                ('rop3', models.DecimalField(verbose_name=b'ROP3', max_digits=6, decimal_places=0)),
                ('people_name', models.CharField(max_length=75)),
                ('fips', models.CharField(max_length=2, verbose_name=b'FIPS')),
                ('fips_of_origin', models.CharField(default=b'', max_length=2, verbose_name=b'FIPS of Origin', blank=True)),
                ('latitude', models.DecimalField(max_digits=10, decimal_places=6)),
                ('longitude', models.DecimalField(max_digits=10, decimal_places=6)),
                ('peid_of_origin', models.BigIntegerField(default=0, verbose_name=b'PEID of Origin', blank=0)),
                ('imb_affinity_group', models.CharField(max_length=75, verbose_name=b'IMB Affinity Group')),
            ],
            options={
                'verbose_name': 'IMB People Group',
                'verbose_name_plural': 'IMB People Groups',
            },
        ),
        migrations.CreateModel(
            name='SIL_ISO_639_3',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=3)),
                ('part_2b', models.CharField(max_length=3, blank=True)),
                ('part_2t', models.CharField(max_length=3, blank=True)),
                ('part_1', models.CharField(max_length=2, blank=True)),
                ('scope', models.CharField(max_length=1, choices=[(b'I', b'Individual'), (b'M', b'Macrolanguage'), (b'S', b'Special')])),
                ('language_type', models.CharField(max_length=1, choices=[(b'A', b'Ancient'), (b'C', b'Constructed'), (b'E', b'Extinct'), (b'H', b'Historical'), (b'L', b'Living'), (b'S', b'Special')])),
                ('ref_name', models.CharField(max_length=150)),
                ('comment', models.CharField(max_length=150, blank=True)),
                ('date_imported', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'SIL ISO Code Set',
            },
        ),
        migrations.CreateModel(
            name='WikipediaISOCountry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('english_short_name', models.CharField(max_length=100)),
                ('alpha_2', models.CharField(max_length=2)),
                ('alpha_3', models.CharField(max_length=3)),
                ('numeric_code', models.CharField(max_length=3)),
                ('iso_3166_2_code', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Wikipedia ISO 3166-1 Country',
                'verbose_name_plural': 'Wikipedia ISO 3166-1 Countries',
            },
        ),
        migrations.CreateModel(
            name='WikipediaISOLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_family', models.CharField(max_length=100)),
                ('language_name', models.CharField(max_length=100)),
                ('native_name', models.CharField(max_length=100)),
                ('iso_639_1', models.CharField(max_length=2)),
                ('iso_639_2t', models.CharField(max_length=3, blank=True)),
                ('iso_639_2b', models.CharField(max_length=3, blank=True)),
                ('iso_639_3', models.CharField(max_length=3, blank=True)),
                ('iso_639_9', models.CharField(max_length=4, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('date_imported', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Wikipedia ISO Language',
            },
        ),
    ]
