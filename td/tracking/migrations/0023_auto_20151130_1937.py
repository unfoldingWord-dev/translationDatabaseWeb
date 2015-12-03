# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0022_auto_20151130_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='charter',
            name='modified_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='modified_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='modified_by',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
