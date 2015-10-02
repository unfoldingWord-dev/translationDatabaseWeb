# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0018_auto_20151001_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='publishing_process',
        ),
        migrations.RemoveField(
            model_name='event',
            name='output_target',
        ),
        migrations.AddField(
            model_name='event',
            name='publication',
            field=models.ManyToManyField(to='tracking.Publication', verbose_name=b'Publishing Medium', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='output_target',
            field=models.ManyToManyField(to='tracking.Output', verbose_name=b'Output Target', blank=True),
        ),
    ]
