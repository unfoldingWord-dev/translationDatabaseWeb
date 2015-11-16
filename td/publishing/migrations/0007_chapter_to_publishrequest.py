# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone

from td.publishing.models import PublishRequest, Chapter


class Migration(migrations.Migration):

    dependencies = [
        ('publishing', '0006_official_resource_type_obs'),
    ]

    operations = [
        migrations.AddField(
            model_name='frame',
            name='ref',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='frame',
            name='title',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='ref',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='chapter',
            name='publish_request',
            field=models.ForeignKey(default=None, null=True, to='publishing.PublishRequest'),
        ),
        migrations.AddField(
            model_name='frame',
            name='number',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
