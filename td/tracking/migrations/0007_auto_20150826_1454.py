# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0006_auto_20150825_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charter',
            name='countries',
            field=models.ManyToManyField(to='tracking.Country', blank=True),
        ),
        migrations.AlterField(
            model_name='charter',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
