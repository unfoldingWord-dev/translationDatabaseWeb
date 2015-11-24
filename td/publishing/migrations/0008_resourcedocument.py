# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('td', '0001_initial'),
        ('publishing', '0007_chapter_to_publishrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('json_data', jsonfield.fields.JSONField(default=dict)),
                ('language', models.ForeignKey(to='td.Language')),
                ('publish_request', models.ForeignKey(related_name='documents', to='publishing.PublishRequest')),
                ('resource_type', models.ForeignKey(to='publishing.OfficialResourceType')),
            ],
        ),
    ]
