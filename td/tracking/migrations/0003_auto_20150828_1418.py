# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_remove_charter_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charter',
            name='created_by',
            field=models.CharField(max_length=200),
        ),
    ]
