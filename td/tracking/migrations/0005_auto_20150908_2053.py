# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0004_auto_20150908_2046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='lead_dept',
            new_name='old_lead_dept',
        ),
    ]
