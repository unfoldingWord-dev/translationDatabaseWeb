# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uwadmin', '0006_auto_20150529_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='publishrequest',
            name='requestor_email',
            field=models.EmailField(default=b'', help_text=b'email address to be notified of request status', max_length=75, blank=True),
            preserve_default=True,
        ),
    ]
