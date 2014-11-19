# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0004_auto_20141021_2122'),
        ('td', '0002_auto_20141011_0532'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('country', models.ForeignKey(blank=True, to='imports.EthnologueCountryCode', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
