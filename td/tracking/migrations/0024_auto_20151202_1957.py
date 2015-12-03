# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0023_auto_20151130_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charter',
            name='number',
            field=models.CharField(max_length=10, null=True, verbose_name=b'Project Accounting Number'),
        ),
        migrations.AlterField(
            model_name='event',
            name='networks',
            field=models.ManyToManyField(to='td.Network', blank=True),
        ),
    ]
