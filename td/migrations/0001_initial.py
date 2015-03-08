# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ietf_tag', models.CharField(max_length=100)),
                ('common_name', models.CharField(max_length=100)),
                ('two_letter', models.CharField(max_length=2, blank=True)),
                ('three_letter', models.CharField(max_length=3, blank=True)),
                ('native_name', models.CharField(max_length=100, blank=True)),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Additional Language',
            },
            bases=(models.Model,),
        ),
    ]
