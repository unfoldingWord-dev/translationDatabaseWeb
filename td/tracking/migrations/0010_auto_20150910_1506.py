# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0009_auto_20150910_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='contact_person',
            field=models.CharField(max_length=200),
        ),
    ]
