# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='direction',
            field=models.CharField(default=b'l', max_length=1, choices=[(b'l', b'ltr'), (b'r', b'rtl')]),
            preserve_default=True,
        ),
    ]
