# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charter',
            name='id',
        ),
        migrations.AlterField(
            model_name='charter',
            name='target_lang_ietf',
            field=models.CharField(max_length=200, serialize=False, primary_key=True, choices=[(b'ina', b'ina'), (b'eng', b'eng'), (b'bri', b'bri'), (b'deu', b'deu')]),
        ),
    ]
