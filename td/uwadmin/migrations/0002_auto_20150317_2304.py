# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uwadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openbiblestory',
            name='checking_entity',
            field=models.ManyToManyField(related_name='resource_publications', to='uwadmin.Organization', blank=True),
            preserve_default=True,
        ),
    ]
