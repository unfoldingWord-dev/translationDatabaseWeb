# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
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
            },
            bases=(models.Model,),
        ),
    ]
