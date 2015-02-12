# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('td', '0003_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='country',
        ),
        migrations.DeleteModel(
            name='Language',
        ),
    ]
