# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0006_auto_20150819_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='lead_dept',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
