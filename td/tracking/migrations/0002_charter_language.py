# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('td', '0001_initial'),
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='charter',
            name='language',
            field=models.ForeignKey(blank=True, to='td.Language', null=True),
        ),
    ]
