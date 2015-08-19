# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0005_department_facilitator_network_translator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='charter',
            old_name='gw_lag_ietf',
            new_name='gw_lang_ietf',
        ),
    ]
