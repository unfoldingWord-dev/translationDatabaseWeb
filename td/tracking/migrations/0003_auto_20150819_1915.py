# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_auto_20150819_1842'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charter',
            fields=[
                ('proj_num', models.SlugField(serialize=False, primary_key=True)),
                ('lang_name', models.CharField(max_length=200, choices=[(b'indonesian', b'Bahasa Indonesia'), (b'english', b'English (American)'), (b'british', b'English (British)'), (b'german', b'German')])),
                ('lang_ietf', models.SlugField(choices=[(b'ina', b'ina'), (b'eng', b'eng'), (b'bri', b'bri'), (b'deu', b'deu')])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('lead_dept', models.CharField(max_length=200)),
                ('gw_lang_name', models.CharField(max_length=50, choices=[(b'indonesian', b'Bahasa Indonesia'), (b'english', b'English (American)'), (b'british', b'English (British)'), (b'german', b'German')])),
                ('gw_lag_ietf', models.CharField(max_length=50, choices=[(b'ina', b'ina'), (b'eng', b'eng'), (b'bri', b'bri'), (b'deu', b'deu')])),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('output_target', models.SlugField()),
                ('translation_method', models.SlugField(choices=[(b'lit', b'literal'), (b'dyn', b'dynamic'), (b'other', b'other')])),
                ('tech_used', models.SlugField(choices=[(b'btak', b'btak'), (b'tk', b'trasnlation keyboard'), (b'other', b'other')])),
                ('comp_tech_used', models.SlugField()),
                ('pub_process', models.TextField(max_length=1500)),
                ('follow_up', models.CharField(max_length=50)),
                ('charter', models.ForeignKey(to='tracking.Charter')),
            ],
        ),
        migrations.DeleteModel(
            name='ProjectCharter',
        ),
    ]
