# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('td', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ['con_src'],
            },
        ),
        migrations.CreateModel(
            name='ConnectionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name of Connection Type')),
                ('mutual', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name of contact')),
                ('email', models.CharField(max_length=255, verbose_name=b'Email address', blank=True)),
                ('d43username', models.CharField(max_length=255, verbose_name=b'Door43 username', blank=True)),
                ('location', models.CharField(max_length=255, blank=True)),
                ('phone', models.CharField(max_length=255, verbose_name=b'Phone number', blank=True)),
                ('other', models.TextField(verbose_name=b'Other information', blank=True)),
                ('languages', models.ManyToManyField(related_name='contacts', to='td.Language')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='LicenseAgreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.FileField(upload_to=b'agreements/')),
            ],
        ),
        migrations.CreateModel(
            name='OfficialResource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_started', models.DateField()),
                ('notes', models.TextField(blank=True)),
                ('offline', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('publish_date', models.DateField(null=True, blank=True)),
                ('version', models.CharField(max_length=10, blank=True)),
                ('source_version', models.CharField(max_length=10, blank=True)),
                ('checking_level', models.IntegerField(blank=True, null=True, choices=[(1, b'1'), (2, b'2'), (3, b'3')])),
            ],
            options={
                'ordering': ['language', 'contact'],
            },
        ),
        migrations.CreateModel(
            name='OfficialResourceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(help_text=b'a 5 character identification code', max_length=5)),
                ('long_name', models.CharField(help_text=b'a more descriptive name', max_length=50)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name of Organization')),
                ('email', models.CharField(max_length=255, verbose_name=b'Email address', blank=True)),
                ('phone', models.CharField(max_length=255, verbose_name=b'Phone number', blank=True)),
                ('website', models.CharField(max_length=255, blank=True)),
                ('location', models.CharField(max_length=255, blank=True)),
                ('other', models.TextField(verbose_name=b'Other information', blank=True)),
                ('checking_entity', models.BooleanField(default=False)),
                ('languages', models.ManyToManyField(related_name='organizations', to='td.Language')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PublishRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('requestor', models.CharField(max_length=100, verbose_name=b'Requester name')),
                ('checking_level', models.IntegerField(verbose_name=b'Requested checking level', choices=[(1, b'1'), (2, b'2'), (3, b'3')])),
                ('source_version', models.CharField(max_length=10, blank=True)),
                ('contributors', models.TextField(help_text=b'Names or Pseudonyms', blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_at', models.DateTimeField(default=None, null=True, db_index=True, blank=True)),
                ('requestor_email', models.EmailField(default=b'', help_text=b'email address to be notified of request status', max_length=254, verbose_name=b'Requester email', blank=True)),
                ('language', models.ForeignKey(related_name='publish_requests', to='td.Language')),
                ('resource_type', models.ForeignKey(to='publishing.OfficialResourceType', null=True)),
                ('source_text', models.ForeignKey(related_name='source_publish_requests', to='td.Language', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecentCommunication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('communication', models.TextField(verbose_name=b'Message', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('contact', models.ForeignKey(related_name='recent_communications', to='publishing.Contact')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['contact', 'created'],
            },
        ),
        migrations.AddField(
            model_name='officialresource',
            name='checking_entity',
            field=models.ManyToManyField(related_name='resource_publications', to='publishing.Organization', blank=True),
        ),
        migrations.AddField(
            model_name='officialresource',
            name='contact',
            field=models.ForeignKey(related_name='official_resources', blank=True, to='publishing.Contact', null=True),
        ),
        migrations.AddField(
            model_name='officialresource',
            name='contributors',
            field=models.ManyToManyField(related_name='+', to='publishing.Contact', blank=True),
        ),
        migrations.AddField(
            model_name='officialresource',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='officialresource',
            name='language',
            field=models.ForeignKey(related_name='official_resources', verbose_name=b'Language', to='td.Language'),
        ),
        migrations.AddField(
            model_name='officialresource',
            name='resource_type',
            field=models.ForeignKey(verbose_name=b'official_resources', to='publishing.OfficialResourceType'),
        ),
        migrations.AddField(
            model_name='officialresource',
            name='source_text',
            field=models.ForeignKey(related_name='+', blank=True, to='td.Language', null=True),
        ),
        migrations.AddField(
            model_name='licenseagreement',
            name='publish_request',
            field=models.ForeignKey(to='publishing.PublishRequest'),
        ),
        migrations.AddField(
            model_name='contact',
            name='org',
            field=models.ManyToManyField(to='publishing.Organization', verbose_name=b'organizations', blank=True),
        ),
        migrations.AddField(
            model_name='connection',
            name='con_dst',
            field=models.ForeignKey(related_name='destination_connections', verbose_name=b'Connection', to='publishing.Contact'),
        ),
        migrations.AddField(
            model_name='connection',
            name='con_src',
            field=models.ForeignKey(related_name='source_connections', to='publishing.Contact'),
        ),
        migrations.AddField(
            model_name='connection',
            name='con_type',
            field=models.ForeignKey(verbose_name=b'Type', to='publishing.ConnectionType'),
        ),
        migrations.AddField(
            model_name='comment',
            name='official_resource',
            field=models.ForeignKey(related_name='comments', to='publishing.OfficialResource', null=True),
        ),
    ]
