# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charter',
            name='number',
            field=models.CharField(max_length=10, verbose_name=b'Project Accounting Number'),
        ),
    ]
