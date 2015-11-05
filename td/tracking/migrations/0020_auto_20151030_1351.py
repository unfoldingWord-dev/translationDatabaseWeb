# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0019_auto_20151002_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='departments',
            field=models.ManyToManyField(related_name='event_supporting_dept', verbose_name=b'Supporting Departments', to='tracking.Department', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='hardware',
            field=models.ManyToManyField(to='tracking.Hardware', verbose_name=b'Hardware Used', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='software',
            field=models.ManyToManyField(to='tracking.Software', verbose_name=b'Software/App Used', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='translation_methods',
            field=models.ManyToManyField(to='tracking.TranslationMethod', verbose_name=b'Translation Methodologies', blank=True),
        ),
    ]
