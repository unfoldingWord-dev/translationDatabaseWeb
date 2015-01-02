# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wycliffe', '0003_auto_20141229_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='gateway_dialect',
            field=models.ForeignKey(related_name='+', blank=True, to='td.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='language',
            name='native_speakers',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='language',
            name='networks_translating',
            field=models.ManyToManyField(to='wycliffe.Network', null=True, blank=True),
            preserve_default=True,
        ),
    ]
