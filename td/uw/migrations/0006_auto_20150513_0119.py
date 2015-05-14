# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uw', '0005_auto_20150408_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='medias',
            field=models.ManyToManyField(to='uw.Media', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('title', 'language')]),
        ),
        migrations.RemoveField(
            model_name='resource',
            name='media',
        ),
    ]
