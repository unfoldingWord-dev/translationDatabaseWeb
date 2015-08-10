# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_language_direction'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='iso_639_3',
            field=models.CharField(default=b'', max_length=3, db_index=True, blank=True),
            preserve_default=True,
        ),
    ]
