# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
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
                ('direction', models.CharField(default=b'l', max_length=1, choices=[(b'l', b'ltr'), (b'r', b'rtl')])),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Additional Language',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=2)),
                ('alpha_3_code', models.CharField(default=b'', max_length=3, blank=True)),
                ('name', models.CharField(max_length=75)),
                ('population', models.IntegerField(null=True, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default=dict, blank=True)),
            ],
            options={
                'db_table': 'uw_country',
            },
        ),
        migrations.CreateModel(
            name='CountryEAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=250)),
                ('source_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('entity', models.ForeignKey(related_name='attributes', to='td.Country')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'uw_countryeav',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=100)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('native_speakers', models.IntegerField(null=True, blank=True)),
                ('gateway_flag', models.BooleanField(default=False, db_index=True)),
                ('direction', models.CharField(default=b'l', max_length=1, choices=[(b'l', b'ltr'), (b'r', b'rtl')])),
                ('iso_639_3', models.CharField(default=b'', max_length=3, verbose_name=b'ISO-639-3', db_index=True, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(default=dict, blank=True)),
                ('country', models.ForeignKey(blank=True, to='td.Country', null=True)),
                ('gateway_language', models.ForeignKey(related_name='gateway_to', blank=True, to='td.Language', null=True)),
            ],
            options={
                'db_table': 'uw_language',
            },
        ),
        migrations.CreateModel(
            name='LanguageEAV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=250)),
                ('source_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('entity', models.ForeignKey(related_name='attributes', to='td.Language')),
                ('source_ct', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'uw_languageeav',
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'uw_network',
            },
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
                'db_table': 'uw_region',
            },
        ),
        migrations.AddField(
            model_name='language',
            name='networks_translating',
            field=models.ManyToManyField(to='td.Network', db_table=b'uw_language_networks_translating', blank=True),
        ),
        migrations.AddField(
            model_name='country',
            name='primary_networks',
            field=models.ManyToManyField(to='td.Network', db_table=b'uw_country_primary_networks', blank=True),
        ),
        migrations.AddField(
            model_name='country',
            name='region',
            field=models.ForeignKey(related_name='countries', blank=True, to='td.Region', null=True),
        ),
    ]
