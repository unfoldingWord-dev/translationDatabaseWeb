# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='translation_method',
            new_name='translation_services',
        ),
        migrations.AlterField(
            model_name='event',
            name='departments',
            field=models.ManyToManyField(help_text=b'Supporting Departments', related_name='event_supporting_dept', to='tracking.Department'),
        ),
        migrations.AlterField(
            model_name='event',
            name='output_target',
            field=models.TextField(max_length=1500, blank=True),
        ),
    ]
