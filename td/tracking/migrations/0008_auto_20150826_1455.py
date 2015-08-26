# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0007_auto_20150826_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charter',
            name='number',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
