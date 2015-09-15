# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publishing', '0002_auto_20150813_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishrequest',
            name='checking_level',
            field=models.IntegerField(verbose_name=b'Requested checking level', choices=[(1, b'1'), (2, b'2'), (3, b'3')]),
        ),
        migrations.AlterField(
            model_name='publishrequest',
            name='contributors',
            field=models.TextField(help_text=b'Names or Pseudonyms', blank=True),
        ),
        migrations.AlterField(
            model_name='publishrequest',
            name='requestor',
            field=models.CharField(max_length=100, verbose_name=b'Requester name'),
        ),
        migrations.AlterField(
            model_name='publishrequest',
            name='requestor_email',
            field=models.EmailField(default=b'', help_text=b'email address to be notified of request status', max_length=254, verbose_name=b'Requester email', blank=True),
        ),
    ]
