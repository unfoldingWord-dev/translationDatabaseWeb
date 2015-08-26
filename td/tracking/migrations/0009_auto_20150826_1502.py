# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0008_auto_20150826_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charter',
            name='start_date',
            field=models.DateField(),
        ),
    ]
