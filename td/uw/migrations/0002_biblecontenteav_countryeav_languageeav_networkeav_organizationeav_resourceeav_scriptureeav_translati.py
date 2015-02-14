# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('uw', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BibleContentEAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=250)),
                ('source_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('entity', models.ForeignKey(to='uw.BibleContent')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CountryEAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=250)),
                ('source_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('entity', models.ForeignKey(to='uw.Country')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LanguageEAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=250)),
                ('source_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('entity', models.ForeignKey(to='uw.Language')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NetworkEAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=250)),
                ('source_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('entity', models.ForeignKey(to='uw.Network')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationEAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=250)),
                ('source_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('entity', models.ForeignKey(to='uw.Organization')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceEAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=250)),
                ('source_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('entity', models.ForeignKey(to='uw.Resource')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScriptureEAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=250)),
                ('source_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('entity', models.ForeignKey(to='uw.Scripture')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TranslationNeedEAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=250)),
                ('source_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('entity', models.ForeignKey(to='uw.TranslationNeed')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TranslatorEAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=250)),
                ('source_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('entity', models.ForeignKey(to='uw.Translator')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkInProgressEAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=250)),
                ('source_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('entity', models.ForeignKey(to='uw.WorkInProgress')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
