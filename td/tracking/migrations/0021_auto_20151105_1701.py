# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0020_auto_20151030_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='publication',
            field=models.ManyToManyField(to='tracking.Publication', verbose_name=b'Distribution Method', blank=True),
        ),
    ]
