# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=2)),
                ('name', models.CharField(max_length=75)),
                ('population', models.IntegerField(null=True, blank=True)),
            ],
            options={
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
                ('entity', models.ForeignKey(related_name='attributes', to='uw.Country')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=100)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('native_speakers', models.IntegerField(null=True, blank=True)),
                ('gateway_flag', models.BooleanField(default=False, db_index=True)),
                ('country', models.ForeignKey(blank=True, to='uw.Country', null=True)),
                ('gateway_language', models.ForeignKey(related_name='gateway_to', blank=True, to='uw.Language', null=True)),
            ],
            options={
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
                ('entity', models.ForeignKey(related_name='attributes', to='uw.Language')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name_plural': 'Media',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('slug', models.SlugField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published_flag', models.BooleanField(default=True, db_index=True)),
                ('extra_data', jsonfield.fields.JSONField(default=dict, blank=True)),
                ('language', models.ForeignKey(related_name='resources', to='uw.Language')),
                ('media', models.ForeignKey(blank=True, to='uw.Media', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('extra_data', jsonfield.fields.JSONField(default=dict, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='resource',
            name='title',
            field=models.ForeignKey(related_name='versions', to='uw.Title'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('title', 'language', 'media')]),
        ),
        migrations.AddField(
            model_name='language',
            name='networks_translating',
            field=models.ManyToManyField(to='uw.Network', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='country',
            name='primary_networks',
            field=models.ManyToManyField(to='uw.Network', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='country',
            name='region',
            field=models.ForeignKey(related_name='countries', blank=True, to='uw.Region', null=True),
            preserve_default=True,
        ),
    ]
