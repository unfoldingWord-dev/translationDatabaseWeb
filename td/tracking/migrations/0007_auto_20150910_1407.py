# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0006_auto_20150910_1359'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='comp_tech_used',
        ),
        migrations.AddField(
            model_name='event',
            name='hardware_used',
            field=models.ManyToManyField(to='tracking.Hardware', verbose_name=b'Hardware Used', blank=True),
        ),
    ]
