# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_auto_20150825_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='departments',
            field=models.ManyToManyField(to='tracking.Department'),
        ),
        migrations.AddField(
            model_name='event',
            name='facilitators',
            field=models.ManyToManyField(to='tracking.Facilitator'),
        ),
        migrations.AddField(
            model_name='event',
            name='materials',
            field=models.ManyToManyField(to='tracking.Material'),
        ),
        migrations.AddField(
            model_name='event',
            name='networks',
            field=models.ManyToManyField(to='tracking.Network'),
        ),
        migrations.AddField(
            model_name='event',
            name='translators',
            field=models.ManyToManyField(to='tracking.Translator'),
        ),
        migrations.AlterField(
            model_name='charter',
            name='entry_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='charter',
            name='start_date',
            field=models.DateField(),
        ),
    ]
