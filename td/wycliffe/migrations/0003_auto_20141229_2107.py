# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wycliffe', '0002_auto_20141209_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scripture',
            name='wip',
            field=models.ForeignKey(verbose_name=b'Work in Progress', blank=True, to='wycliffe.WorkInProgress', null=True),
            preserve_default=True,
        ),
    ]
