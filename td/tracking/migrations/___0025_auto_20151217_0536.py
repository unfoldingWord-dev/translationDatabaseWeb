# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0024_auto_20151202_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charter',
            name='number',
            field=models.CharField(verbose_name=b'Project Accounting Number', blank=True, default='', max_length=10),
            preserve_default=False,
        ),
    ]
