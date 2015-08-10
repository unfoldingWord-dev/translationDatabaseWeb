# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ['con_src'],
            },
            bases=(models.Model,),
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
            bases=(models.Model,),
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
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LangCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('langcode', models.CharField(unique=True, max_length=25, verbose_name=b'Language Code')),
                ('langname', models.CharField(max_length=255, verbose_name=b'Language Name')),
                ('checking_level', models.IntegerField(null=True)),
            ],
            options={
                'ordering': ['langcode'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OpenBibleStory',
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
                ('checking_entity', models.ManyToManyField(related_name='resource_publications', to='publishing.Contact', blank=True)),
                ('contact', models.ForeignKey(related_name='open_bible_stories', to='publishing.Contact')),
                ('contributors', models.ManyToManyField(related_name='+', to='publishing.Contact', blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('language', models.OneToOneField(related_name='open_bible_story', verbose_name=b'Language', to='publishing.LangCode')),
                ('source_text', models.ForeignKey(related_name='+', blank=True, to='publishing.LangCode', null=True)),
            ],
            options={
                'ordering': ['language', 'contact'],
            },
            bases=(models.Model,),
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
                ('languages', models.ManyToManyField(related_name='organizations', to='publishing.LangCode')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
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
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contact',
            name='languages',
            field=models.ManyToManyField(related_name='contacts', to='publishing.LangCode'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='org',
            field=models.ManyToManyField(to='publishing.Organization', verbose_name=b'organizations', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='connection',
            name='con_dst',
            field=models.ForeignKey(related_name='destination_connections', verbose_name=b'Connection', to='publishing.Contact'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='connection',
            name='con_src',
            field=models.ForeignKey(related_name='source_connections', to='publishing.Contact'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='connection',
            name='con_type',
            field=models.ForeignKey(verbose_name=b'Type', to='publishing.ConnectionType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='open_bible_story',
            field=models.ForeignKey(related_name='comments', to='publishing.OpenBibleStory'),
            preserve_default=True,
        ),
    ]
