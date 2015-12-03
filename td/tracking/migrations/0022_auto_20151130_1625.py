# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0021_auto_20151105_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='charter',
            name='modified_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='charter',
            name='modified_by',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='modified_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='modified_by',
            field=models.CharField(default=b'unknown', max_length=200, blank=True),
        ),
    ]
