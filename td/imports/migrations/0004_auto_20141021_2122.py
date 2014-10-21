# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0003_ethnologuecountrycode_ethnologuelanguagecode_ethnologuelanguageindex'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ethnologuelanguageindex',
            options={'verbose_name': 'Ethnologue Language Index', 'verbose_name_plural': 'Ethnologue Language Index'},
        ),
    ]
