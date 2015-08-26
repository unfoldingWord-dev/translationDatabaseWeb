# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0009_auto_20150826_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charter',
            name='created_by',
            field=models.CharField(default=b'unknown', max_length=200),
        ),
    ]
