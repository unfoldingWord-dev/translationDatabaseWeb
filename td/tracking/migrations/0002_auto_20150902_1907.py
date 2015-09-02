# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charter',
            name='lead_dept',
        ),
        migrations.AddField(
            model_name='charter',
            name='lead_dept',
            field=models.ManyToManyField(to='tracking.Department', verbose_name=b'Lead Department'),
        ),
    ]
