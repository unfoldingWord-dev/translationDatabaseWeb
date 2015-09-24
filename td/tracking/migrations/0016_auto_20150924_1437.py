# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0015_event_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='number',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
    ]
