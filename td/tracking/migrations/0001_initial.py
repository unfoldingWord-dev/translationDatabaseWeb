# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Charter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('number', models.CharField(unique=True, max_length=50, blank=True)),
                ('target_lang_ietf', models.CharField(max_length=200, choices=[(b'ina', b'ina'), (b'eng', b'eng'), (b'bri', b'bri'), (b'deu', b'deu')])),
                ('target_lang_name', models.CharField(max_length=100, choices=[(b'indonesian', b'Bahasa Indonesia'), (b'english', b'English (American)'), (b'british', b'English (British)'), (b'german', b'German')])),
                ('gw_lang_ietf', models.SlugField(choices=[(b'ina', b'ina'), (b'eng', b'eng'), (b'bri', b'bri'), (b'deu', b'deu')])),
                ('gw_lang_name', models.CharField(max_length=100, choices=[(b'indonesian', b'Bahasa Indonesia'), (b'english', b'English (American)'), (b'british', b'English (British)'), (b'german', b'German')])),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(blank=True)),
                ('lead_dept', models.CharField(max_length=200, blank=True)),
                ('entry_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('username', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(max_length=200, blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True)),
                ('lead_dept', models.CharField(max_length=200, blank=True)),
                ('output_target', models.SlugField(blank=True, choices=[(b'print', b'print'), (b'audio', b'audio'), (b'other', b'other')])),
                ('translation_method', models.SlugField(blank=True, choices=[(b'lit', b'literal'), (b'dyn', b'dynamic'), (b'other', b'other')])),
                ('tech_used', models.SlugField(blank=True, choices=[(b'btak', b'btak'), (b'tk', b'trasnlation keyboard'), (b'other', b'other')])),
                ('comp_tech_used', models.SlugField(blank=True, choices=[(b'btak', b'btak'), (b'tk', b'trasnlation keyboard'), (b'other', b'other')])),
                ('pub_process', models.TextField(max_length=1500, blank=True)),
                ('follow_up', models.CharField(max_length=200, blank=True)),
                ('charter', models.ForeignKey(to='tracking.Charter')),
            ],
        ),
        migrations.CreateModel(
            name='Facilitator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('is_lead', models.BooleanField(default=False)),
                ('speaks_gl', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('ietf', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('licensed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Translator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
