# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0012_auto_20150910_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvtFac',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(to='tracking.Event')),
                ('facilitator', models.ForeignKey(to='tracking.Facilitator')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='facilitators2',
            field=models.ManyToManyField(related_name='event_facilitator2', through='tracking.EvtFac', to='tracking.Facilitator', blank=True),
        ),
    ]
