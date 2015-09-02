# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('td', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(verbose_name=b'Start Date')),
                ('end_date', models.DateField(null=True, verbose_name=b'Projected Completion Date')),
                ('number', models.CharField(max_length=50, verbose_name=b'Project Accounting Number')),
                ('lead_dept', models.CharField(max_length=200, verbose_name=b'Lead Department')),
                ('contact_person', models.CharField(max_length=200, null=True, verbose_name=b'Follow-up Person')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(max_length=200)),
                ('countries', models.ManyToManyField(help_text=b'Hold Ctrl while clicking to select multiple countries', to='td.Country', verbose_name=b'Countries that speak this language')),
                ('language', models.OneToOneField(verbose_name=b'Target Language', to='td.Language')),
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
    ]
