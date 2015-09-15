# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0005_auto_20150910_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='tech_used',
        ),
        migrations.AlterField(
            model_name='event',
            name='translation_services',
            field=models.ManyToManyField(to='tracking.TranslationService', verbose_name=b'Translation Services', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='software_used',
            field=models.ManyToManyField(to='tracking.Software', verbose_name=b'Software/App Used', blank=True),
        ),
    ]
