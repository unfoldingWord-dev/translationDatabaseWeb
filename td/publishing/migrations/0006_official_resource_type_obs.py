# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("publishing", "0005_chapter_frame"),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialresource',
            name='resource_type',
            field=models.ForeignKey(
                verbose_name=b'Official resource type',
                to='publishing.OfficialResourceType'
            ),
        ),
        migrations.AlterField(
            model_name='publishrequest',
            name='resource_type',
            field=models.ForeignKey(
                verbose_name=b'Official resource type',
                to='publishing.OfficialResourceType',
                null=True
            ),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='ref',
            field=models.TextField(),
        ),  
        migrations.AlterField(
            model_name='chapter',
            name='title',
            field=models.TextField(),
        ),  
        migrations.AlterField(
            model_name='frame',
            name='identifier',
            field=models.TextField(),
        ),  
        migrations.AlterField(
            model_name='frame',
            name='img',
            field=models.URLField(),
        ),  
    ]
