# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikipediaISOCountry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('english_short_name', models.CharField(max_length=100)),
                ('alpha_2', models.CharField(max_length=2)),
                ('alpha_3', models.CharField(max_length=3)),
                ('numeric_code', models.CharField(max_length=3)),
                ('iso_3166_2_code', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Wikipedia ISO 3166-1 Country',
                'verbose_name_plural': 'Wikipedia ISO 3166-1 Countries',
            },
            bases=(models.Model,),
        ),
    ]
