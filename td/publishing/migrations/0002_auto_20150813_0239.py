# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('td', '0001_initial'),
        ('publishing', '0001_initial'),
    ]

    operations = [
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
                ('checking_entity', models.ManyToManyField(related_name='resource_publications', to='publishing.Organization', blank=True)),
                ('contact', models.ForeignKey(related_name='official_resources', blank=True, to='publishing.Contact', null=True)),
                ('contributors', models.ManyToManyField(related_name='+', to='publishing.Contact', blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(related_name='official_resources', verbose_name=b'Language', to='td.Language')),
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
        migrations.RemoveField(
            model_name='openbiblestory',
            name='checking_entity',
        ),
        migrations.RemoveField(
            model_name='openbiblestory',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='openbiblestory',
            name='contributors',
        ),
        migrations.RemoveField(
            model_name='openbiblestory',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='openbiblestory',
            name='language',
        ),
        migrations.RemoveField(
            model_name='openbiblestory',
            name='source_text',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='open_bible_story',
        ),
        migrations.RemoveField(
            model_name='publishrequest',
            name='resource',
        ),
        migrations.DeleteModel(
            name='OpenBibleStory',
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
            model_name='comment',
            name='official_resource',
            field=models.ForeignKey(related_name='comments', to='publishing.OfficialResource', null=True),
        ),
        migrations.AddField(
            model_name='publishrequest',
            name='resource_type',
            field=models.ForeignKey(to='publishing.OfficialResourceType', null=True),
        ),
    ]
