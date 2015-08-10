# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0007_auto_20150515_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='copyright_year',
            field=models.IntegerField(default=None, null=True, verbose_name=b'copyright', db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='published_date',
            field=models.DateField(default=None, null=True, db_index=True, blank=True),
            preserve_default=True,
        ),
    ]
