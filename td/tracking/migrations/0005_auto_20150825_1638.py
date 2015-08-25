# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0004_charter_countries'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charter',
            name='entry_date',
        ),
        migrations.AddField(
            model_name='charter',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
