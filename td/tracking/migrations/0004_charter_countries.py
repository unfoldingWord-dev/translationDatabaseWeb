# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0003_auto_20150825_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='charter',
            name='countries',
            field=models.ManyToManyField(to='tracking.Country'),
        ),
    ]
