# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0016_auto_20150924_1437'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TranslationService',
            new_name='TranslationMethod',
        ),
        migrations.RemoveField(
            model_name='event',
            name='translation_services',
        ),
        migrations.AddField(
            model_name='event',
            name='translation_methods',
            field=models.ManyToManyField(help_text=b'Hold Ctrl while clicking to select multiple items', to='tracking.TranslationMethod', verbose_name=b'Translation Methodologies', blank=True),
        ),
    ]
