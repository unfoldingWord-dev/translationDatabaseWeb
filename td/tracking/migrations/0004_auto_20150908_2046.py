# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0003_auto_20150908_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(verbose_name=b'Projected Completion Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='lead_dept',
            field=models.CharField(max_length=200, verbose_name=b'Lead Department'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(verbose_name=b'Start Date'),
        ),
    ]
