# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0008_auto_20150910_1410'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='hardware_used',
            new_name='hardware',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='pub_process',
            new_name='publishing_process',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='software_used',
            new_name='software',
        ),
    ]
