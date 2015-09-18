# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('td', '0001_initial'),
        ('publishing', '0004_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('ref', models.CharField(max_length=300)),
                ('title', models.CharField(max_length=300)),
                ('language', models.ForeignKey(to='td.Language')),
                ('resource_type', models.ForeignKey(to='publishing.OfficialResourceType')),
            ],
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=10)),
                ('img', models.URLField(max_length=300)),
                ('text', models.TextField()),
                ('chapter', models.ForeignKey(to='publishing.Chapter')),
            ],
        ),
    ]
