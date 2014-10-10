# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SIL_ISO_639_3',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=3)),
                ('part_2b', models.CharField(max_length=3, blank=True)),
                ('part_2t', models.CharField(max_length=3, blank=True)),
                ('part_1', models.CharField(max_length=2, blank=True)),
                ('scope', models.CharField(max_length=1, choices=[(b'I', b'Individual'), (b'M', b'Macrolanguage'), (b'S', b'Special')])),
                ('language_type', models.CharField(max_length=1, choices=[(b'A', b'Ancient'), (b'C', b'Constructed'), (b'E', b'Extinct'), (b'H', b'Historical'), (b'L', b'Living'), (b'S', b'Special')])),
                ('ref_name', models.CharField(max_length=150)),
                ('comment', models.CharField(max_length=150, blank=True)),
                ('date_imported', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'SIL ISO Code Set',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='wikipediaisolanguage',
            options={'verbose_name': 'Wikipedia ISO Language'},
        ),
    ]
