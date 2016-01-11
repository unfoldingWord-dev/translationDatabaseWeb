# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0024_auto_20151202_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='translator',
            name='sof',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='translator',
            name='tg',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='charter',
            name='number',
            field=models.CharField(default=b'', max_length=10, verbose_name=b'Project Accounting Number', blank=True),
        ),
    ]
