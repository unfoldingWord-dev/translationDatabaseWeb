# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0025_auto_20151209_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translator',
            name='sof',
        ),
        migrations.RemoveField(
            model_name='translator',
            name='tg',
        ),
        migrations.AddField(
            model_name='translator',
            name='docs_signed',
            field=models.BooleanField(default=False),
        ),
    ]
