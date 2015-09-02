# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0003_auto_20150828_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='charter',
            name='contact_person',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Follow-up Person'),
        ),
        migrations.AlterField(
            model_name='charter',
            name='countries',
            field=models.ManyToManyField(help_text=b'Hold Ctrl while clicking to select multiple countries', to='td.Country', verbose_name=b'Countries that speak this language'),
        ),
        migrations.AlterField(
            model_name='charter',
            name='end_date',
            field=models.DateField(null=True, verbose_name=b'Projected Completion Date'),
        ),
        migrations.AlterField(
            model_name='charter',
            name='lead_dept',
            field=models.CharField(max_length=200, verbose_name=b'Lead Department'),
        ),
        migrations.AlterField(
            model_name='charter',
            name='number',
            field=models.CharField(max_length=50, verbose_name=b'Project Accounting Number'),
        ),
    ]
