# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0010_auto_20150910_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='created_by',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='departments',
            field=models.ManyToManyField(help_text=b'Hold Ctrl while clicking to select multiple items', related_name='event_supporting_dept', verbose_name=b'Supporting Departments', to='tracking.Department', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='hardware',
            field=models.ManyToManyField(help_text=b'Hold Ctrl while clicking to select multiple items', to='tracking.Hardware', verbose_name=b'Hardware Used', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='networks',
            field=models.ManyToManyField(help_text=b'Hold Ctrl while clicking to select multiple items', to='td.Network', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='software',
            field=models.ManyToManyField(help_text=b'Hold Ctrl while clicking to select multiple items', to='tracking.Software', verbose_name=b'Software/App Used', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='translation_services',
            field=models.ManyToManyField(help_text=b'Hold Ctrl while clicking to select multiple items', to='tracking.TranslationService', verbose_name=b'Translation Services', blank=True),
        ),
    ]
