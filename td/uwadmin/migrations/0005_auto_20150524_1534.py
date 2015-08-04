# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uwadmin', '0004_auto_20150318_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='publishrequest',
            name='approved_at',
            field=models.DateTimeField(default=None, null=True, db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publishrequest',
            name='source_text',
            field=models.ForeignKey(related_name='source_publish_requests', to='uwadmin.LangCode', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publishrequest',
            name='source_version',
            field=models.CharField(max_length=10, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publishrequest',
            name='language',
            field=models.ForeignKey(related_name='publish_requests', to='uwadmin.LangCode'),
            preserve_default=True,
        ),
    ]
