# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0002_auto_20141010_1718'),
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
            bases=(models.Model,),
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
            bases=(models.Model,),
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
            },
            bases=(models.Model,),
        ),
    ]
