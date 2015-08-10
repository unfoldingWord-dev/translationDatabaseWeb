# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('publishing', '0003_langcode_gateway_flag'),
    ]

    operations = [
        migrations.CreateModel(
            name='LicenseAgreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.FileField(upload_to=b'agreements/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublishRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('requestor', models.CharField(max_length=100)),
                ('resource', models.CharField(default=b'obs', max_length=20, choices=[(b'obs', b'Open Bible Stories')])),
                ('checking_level', models.IntegerField(choices=[(1, b'1'), (2, b'2'), (3, b'3')])),
                ('contributors', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('language', models.ForeignKey(to='publishing.LangCode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='licenseagreement',
            name='publish_request',
            field=models.ForeignKey(to='publishing.PublishRequest'),
            preserve_default=True,
        ),
    ]
