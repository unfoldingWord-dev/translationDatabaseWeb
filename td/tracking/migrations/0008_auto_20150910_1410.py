# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0007_auto_20150910_1407'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='follow_up',
            new_name='contact_person',
        ),
    ]
