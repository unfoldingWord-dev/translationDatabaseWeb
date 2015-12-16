# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publishing', '0008_resourcedocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='publishrequest',
            name='license_title',
            field=models.TextField(default=b'CC BY-SA 4.0', blank=True, null=False),
        ),
    ]
