# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0005_auto_20150825_1638'),
    ]

    operations = [
        migrations.RenameField(
            model_name='charter',
            old_name='username',
            new_name='created_by',
        ),
    ]
