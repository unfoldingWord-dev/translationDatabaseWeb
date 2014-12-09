# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wycliffe', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Denomination',
            new_name='Network',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='primary_denominations',
            new_name='primary_networks',
        ),
        migrations.RenameField(
            model_name='language',
            old_name='denominations_translating',
            new_name='networks_translating',
        ),
        migrations.AlterField(
            model_name='scripture',
            name='bible_content',
            field=models.ForeignKey(verbose_name=b'Bible Content', to='wycliffe.BibleContent'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scripture',
            name='wip',
            field=models.ForeignKey(verbose_name=b'Work in Progress', to='wycliffe.WorkInProgress'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workinprogress',
            name='bible_content',
            field=models.ForeignKey(verbose_name=b'Bible Content', to='wycliffe.BibleContent'),
            preserve_default=True,
        ),
    ]
