# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-26 20:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commenting', '0002_create_commenttag_and_taggedobject'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentwithtags',
            options={'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
    ]