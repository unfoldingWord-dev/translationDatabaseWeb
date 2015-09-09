# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0005_auto_20150908_2053'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Network',
        ),
        migrations.AlterField(
            model_name='event',
            name='networks',
            field=models.ManyToManyField(to='td.Network'),
        ),
    ]
