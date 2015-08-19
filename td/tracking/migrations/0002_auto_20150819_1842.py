# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectcharter',
            name='id',
        ),
        migrations.AlterField(
            model_name='projectcharter',
            name='proj_num',
            field=models.SlugField(serialize=False, primary_key=True),
        ),
    ]
