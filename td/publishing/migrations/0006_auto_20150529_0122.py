# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publishing', '0005_auto_20150524_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openbiblestory',
            name='contact',
            field=models.ForeignKey(related_name='open_bible_stories', blank=True, to='publishing.Contact', null=True),
            preserve_default=True,
        ),
    ]
