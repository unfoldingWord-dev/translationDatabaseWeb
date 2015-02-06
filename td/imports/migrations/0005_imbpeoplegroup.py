# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0004_auto_20141021_2122'),
    ]

    operations = [
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
            bases=(models.Model,),
        ),
    ]
