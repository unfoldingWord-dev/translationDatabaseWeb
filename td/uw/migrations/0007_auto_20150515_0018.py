# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('uw', '0006_auto_20150513_0119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('extra_data', jsonfield.fields.JSONField(default=dict, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='resource',
            name='publisher',
            field=models.ForeignKey(blank=True, to='uw.Publisher', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='title',
            name='publisher',
            field=models.ForeignKey(blank=True, to='uw.Publisher', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='medias',
            field=models.ManyToManyField(to='uw.Media', verbose_name=b'Media', blank=True),
            preserve_default=True,
        ),
    ]
