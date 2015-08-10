# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publishing', '0002_auto_20150317_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='langcode',
            name='gateway_flag',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
