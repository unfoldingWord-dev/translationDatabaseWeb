# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-01 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('td', '0026_tepmlanguage_delete_name_property'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templanguage',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
