# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0017_auto_20151001_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='current_check_level',
            field=models.SlugField(choices=[(b'1', b'1'), (b'2', b'2'), (b'3', b'3')], blank=True, null=True, verbose_name=b'Current Checking Level'),
        ),
        migrations.AddField(
            model_name='event',
            name='target_check_level',
            field=models.SlugField(choices=[(b'1', b'1'), (b'2', b'2'), (b'3', b'3')], blank=True, null=True, verbose_name=b'Anticipated Checking Level'),
        ),
    ]
