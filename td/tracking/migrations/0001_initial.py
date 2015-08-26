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
                ('target_lang_ietf', models.CharField(max_length=200, serialize=False, verbose_name=b'Target Language IETF Tag', primary_key=True, choices=[(b'ina', b'ina'), (b'eng', b'eng'), (b'bri', b'bri'), (b'deu', b'deu')])),
                ('target_lang_name', models.CharField(max_length=100, verbose_name=b'Target Language Name', choices=[(b'indonesian', b'Bahasa Indonesia'), (b'english', b'English (American)'), (b'british', b'English (British)'), (b'german', b'German')])),
                ('gw_lang_ietf', models.SlugField(verbose_name=b'Gateway Language Tag', choices=[(b'ina', b'ina'), (b'eng', b'eng'), (b'bri', b'bri'), (b'deu', b'deu')])),
                ('gw_lang_name', models.CharField(max_length=100, verbose_name=b'Gateway Language Name', choices=[(b'indonesian', b'Bahasa Indonesia'), (b'english', b'English (American)'), (b'british', b'English (British)'), (b'german', b'German')])),
                ('start_date', models.DateField(verbose_name=b'Start Date')),
                ('end_date', models.DateField(null=True, verbose_name=b'Projected Completion Date', blank=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name=b'Name for this project')),
                ('number', models.CharField(max_length=50, verbose_name=b'Project Accounting Number', blank=True)),
                ('lead_dept', models.CharField(max_length=200, verbose_name=b'Lead Department', blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default=b'unknown', max_length=200)),
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
                ('departments', models.ManyToManyField(to='tracking.Department')),
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
        migrations.AddField(
            model_name='event',
            name='facilitators',
            field=models.ManyToManyField(to='tracking.Facilitator'),
        ),
        migrations.AddField(
            model_name='event',
            name='materials',
            field=models.ManyToManyField(to='tracking.Material'),
        ),
        migrations.AddField(
            model_name='event',
            name='networks',
            field=models.ManyToManyField(to='tracking.Network'),
        ),
        migrations.AddField(
            model_name='event',
            name='translators',
            field=models.ManyToManyField(to='tracking.Translator'),
        ),
        migrations.AddField(
            model_name='charter',
            name='countries',
            field=models.ManyToManyField(to='tracking.Country', verbose_name=b'Countries that speak this language', blank=True),
        ),
    ]
