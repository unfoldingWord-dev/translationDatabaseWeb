# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0014_auto_20150916_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='number',
            field=models.PositiveSmallIntegerField(default=0, null=True, blank=True),
        ),
    ]
