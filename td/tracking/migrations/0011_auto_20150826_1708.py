# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0010_auto_20150826_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charter',
            name='end_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
