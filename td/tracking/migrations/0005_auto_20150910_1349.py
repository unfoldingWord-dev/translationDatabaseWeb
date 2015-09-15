# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0004_auto_20150910_1339'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TranslationServices',
            new_name='TranslationService',
        ),
    ]
