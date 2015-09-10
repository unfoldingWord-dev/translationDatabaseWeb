# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0003_auto_20150910_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='departments',
            field=models.ManyToManyField(help_text=b'Supporting Departments', related_name='event_supporting_dept', to='tracking.Department', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='facilitators',
            field=models.ManyToManyField(to='tracking.Facilitator', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='materials',
            field=models.ManyToManyField(to='tracking.Material', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='networks',
            field=models.ManyToManyField(to='td.Network', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='translators',
            field=models.ManyToManyField(to='tracking.Translator', blank=True),
        ),
    ]
