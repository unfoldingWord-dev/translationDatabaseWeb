# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charter',
            name='gw_lang_ietf',
        ),
        migrations.RemoveField(
            model_name='charter',
            name='gw_lang_name',
        ),
        migrations.RemoveField(
            model_name='charter',
            name='target_lang_ietf',
        ),
        migrations.RemoveField(
            model_name='charter',
            name='target_lang_name',
        ),
        migrations.AlterField(
            model_name='charter',
            name='language',
            field=models.OneToOneField(primary_key=True, serialize=False, to='td.Language', verbose_name=b'Target Language'),
        ),
    ]
