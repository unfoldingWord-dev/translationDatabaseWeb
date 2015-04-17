# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('uw', '0004_auto_20150407_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='alpha_3_code',
            field=models.CharField(default=b'', max_length=3, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='country',
            name='extra_data',
            field=jsonfield.fields.JSONField(default=dict, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='language',
            name='extra_data',
            field=jsonfield.fields.JSONField(default=dict, blank=True),
            preserve_default=True,
        ),
    ]
