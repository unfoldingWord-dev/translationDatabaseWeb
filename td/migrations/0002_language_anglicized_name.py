# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('td', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='anglicized_name',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
