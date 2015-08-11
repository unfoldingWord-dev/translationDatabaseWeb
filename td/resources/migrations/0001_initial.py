# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('td', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
            ],
            options={
                'db_table': 'uw_media',
                'verbose_name_plural': 'Media',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('extra_data', jsonfield.fields.JSONField(default=dict, blank=True)),
            ],
            options={
                'db_table': 'uw_publisher',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published_flag', models.BooleanField(default=True, db_index=True)),
                ('published_date', models.DateField(default=None, null=True, db_index=True, blank=True)),
                ('copyright_year', models.IntegerField(default=None, null=True, verbose_name=b'copyright', db_index=True, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default=dict, blank=True)),
                ('language', models.ForeignKey(related_name='resources', to='td.Language')),
                ('medias', models.ManyToManyField(to='resources.Media', db_table=b'uw_resource_medias', verbose_name=b'Media', blank=True)),
                ('publisher', models.ForeignKey(blank=True, to='resources.Publisher', null=True)),
            ],
            options={
                'db_table': 'uw_resource',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('extra_data', jsonfield.fields.JSONField(default=dict, blank=True)),
                ('publisher', models.ForeignKey(blank=True, to='resources.Publisher', null=True)),
            ],
            options={
                'db_table': 'uw_title',
            },
        ),
        migrations.AddField(
            model_name='resource',
            name='title',
            field=models.ForeignKey(related_name='versions', to='resources.Title'),
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('title', 'language')]),
        ),
    ]
