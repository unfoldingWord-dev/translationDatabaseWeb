# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectCharter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang_name', models.CharField(max_length=200, choices=[(b'indonesian', b'Bahasa Indonesia'), (b'english', b'English (American)'), (b'british', b'English (British)'), (b'german', b'German')])),
                ('lang_ietf', models.SlugField(choices=[(b'ina', b'ina'), (b'eng', b'eng'), (b'bri', b'bri'), (b'deu', b'deu')])),
                ('proj_num', models.SlugField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('lead_dept', models.CharField(max_length=200)),
                ('gw_lang_name', models.CharField(max_length=50, choices=[(b'indonesian', b'Bahasa Indonesia'), (b'english', b'English (American)'), (b'british', b'English (British)'), (b'german', b'German')])),
                ('gw_lag_ietf', models.CharField(max_length=50, choices=[(b'ina', b'ina'), (b'eng', b'eng'), (b'bri', b'bri'), (b'deu', b'deu')])),
            ],
        ),
    ]
