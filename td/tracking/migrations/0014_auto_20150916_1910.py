# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0013_auto_20150916_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evtfac',
            name='event',
        ),
        migrations.RemoveField(
            model_name='evtfac',
            name='facilitator',
        ),
        migrations.RemoveField(
            model_name='event',
            name='facilitators2',
        ),
        migrations.DeleteModel(
            name='EvtFac',
        ),
    ]
