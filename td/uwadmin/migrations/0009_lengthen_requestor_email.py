# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uwadmin', '0008_langcode_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishrequest',
            name='requestor_email',
            field=models.EmailField(default=b'', help_text=b'email address to be notified of request status', max_length=254, blank=True),
        ),
    ]
