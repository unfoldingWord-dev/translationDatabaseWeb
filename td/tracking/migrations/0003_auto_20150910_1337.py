# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_auto_20150910_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranslationServices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='charter',
            field=models.ForeignKey(verbose_name=b'Project Charter', to='tracking.Charter'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(verbose_name=b'End Date'),
        ),
        migrations.RemoveField(
            model_name='event',
            name='translation_services',
        ),
        migrations.AddField(
            model_name='event',
            name='translation_services',
            field=models.ManyToManyField(to='tracking.TranslationServices', blank=True),
        ),
    ]
