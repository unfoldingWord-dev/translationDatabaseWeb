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
                ('end_date', models.DateField(verbose_name=b'Projected Completion Date')),
                ('number', models.CharField(max_length=10, verbose_name=b'Project Accounting Number')),
                ('contact_person', models.CharField(max_length=200, verbose_name=b'Follow-up Person')),
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
                ('location', models.CharField(max_length=200)),
                ('start_date', models.DateField(verbose_name=b'Start Date')),
                ('end_date', models.DateField(verbose_name=b'Projected Completion Date')),
                ('output_target', models.CharField(max_length=200, blank=True)),
                ('translation_method', models.SlugField(blank=True, choices=[(b'church', b'Church group'), (b'door43web', b'Door43 Website'), (b'mast', b'MAST'), (b'seedco', b'Seed Co.'), (b'sovee-memoq', b'Sovee/MemoQ'), (b'translator', b'Translator'), (b'ts', b'translationStudio'), (b'other', b'Other')])),
                ('tech_used', models.SlugField(blank=True, choices=[(b'door43web', b'Door43 Website'), (b'msword', b'Microsoft Word'), (b'paratext', b'ParaText'), (b'sovee-memoq', b'Sovee/MemoQ'), (b'ts', b'translationStudio'), (b'other', b'Other')])),
                ('comp_tech_used', models.SlugField(blank=True, choices=[(b'tablet', b'Tablet'), (b'laptop', b'Laptop'), (b'keyboard-layout', b'Keyboard Layout'), (b'fonts', b'Fonts'), (b'word-template', b'Word Template')])),
                ('pub_process', models.TextField(max_length=1500, blank=True)),
                ('follow_up', models.CharField(max_length=200, blank=True)),
                ('charter', models.ForeignKey(to='tracking.Charter')),
                ('departments', models.ManyToManyField(related_name='event_supporting_dept', to='tracking.Department')),
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
            name='lead_dept',
            field=models.ForeignKey(related_name='event_lead_dept', verbose_name=b'Lead Department', to='tracking.Department'),
        ),
        migrations.AddField(
            model_name='event',
            name='materials',
            field=models.ManyToManyField(to='tracking.Material'),
        ),
        migrations.AddField(
            model_name='event',
            name='networks',
            field=models.ManyToManyField(to='td.Network'),
        ),
        migrations.AddField(
            model_name='event',
            name='translators',
            field=models.ManyToManyField(to='tracking.Translator'),
        ),
        migrations.AddField(
            model_name='charter',
            name='lead_dept',
            field=models.ForeignKey(verbose_name=b'Lead Department', to='tracking.Department'),
        ),
    ]
