# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uwadmin', '0007_publishrequest_requestor_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='langcode',
            name='version',
            field=models.CharField(default=b'', max_length=25),
            preserve_default=True,
        ),
    ]
