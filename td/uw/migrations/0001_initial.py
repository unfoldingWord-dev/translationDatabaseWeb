# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('td', '0003_language'),
        ('imports', '0004_auto_20141021_2122'),
    ]

    operations = [
        migrations.CreateModel(
            name='BibleContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('population', models.IntegerField(null=True, blank=True)),
                ('country', models.ForeignKey(to='imports.EthnologueCountryCode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('native_speakers', models.IntegerField(null=True, blank=True)),
                ('country', models.ForeignKey(to='uw.Country')),
                ('gateway_dialect', models.ForeignKey(related_name='+', blank=True, to='td.Language', null=True)),
                ('living_language', models.ForeignKey(related_name='+', to='td.Language')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(help_text=b'Email address.', max_length=255, blank=True)),
                ('d43username', models.CharField(help_text=b'Door43 username.', max_length=255, blank=True)),
                ('location', models.CharField(help_text=b'Location.', max_length=255, blank=True)),
                ('phone', models.CharField(help_text=b'Phone number.', max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('copyright', models.CharField(max_length=100, blank=True)),
                ('license', models.TextField(blank=True)),
                ('copyright_holder', models.ForeignKey(blank=True, to='uw.Organization', null=True)),
                ('language', models.ForeignKey(to='uw.Language')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scripture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(max_length=50, choices=[(b'full-bible', b'Full Bible'), (b'full-nt', b'Full NT'), (b'portions', b'Bible Portions'), (b'audio', b'Audio'), (b'video', b'Video'), (b'braille', b'Braille'), (b'children', b"Illustrated Children's"), (b'obs', b'Open Bible Stories')])),
                ('year', models.IntegerField()),
                ('publisher', models.CharField(max_length=200)),
                ('bible_content', models.ForeignKey(verbose_name=b'Bible Content', to='uw.BibleContent')),
                ('language', models.ForeignKey(to='uw.Language')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TranslationNeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text_gaps', models.TextField(blank=True)),
                ('text_updates', models.TextField(blank=True)),
                ('other_gaps', models.TextField(blank=True)),
                ('other_updates', models.TextField(blank=True)),
                ('language', models.ForeignKey(to='uw.Language')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Translator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(help_text=b'Email address.', max_length=255, blank=True)),
                ('d43username', models.CharField(help_text=b'Door43 username.', max_length=255, blank=True)),
                ('location', models.CharField(help_text=b'Location.', max_length=255, blank=True)),
                ('phone', models.CharField(help_text=b'Phone number.', max_length=255, blank=True)),
                ('relationship', models.TextField(help_text=b'Relationships to other people or organizations.', blank=True)),
                ('other', models.CharField(help_text=b'Other information.', max_length=255, blank=True)),
                ('languages', models.ManyToManyField(help_text=b'Langauges spoken by contact.', related_name='Contact', to='uw.Language')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkInProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(max_length=50, choices=[(b'full-bible', b'Full Bible'), (b'full-nt', b'Full NT'), (b'portions', b'Bible Portions'), (b'audio', b'Audio'), (b'video', b'Video'), (b'braille', b'Braille'), (b'children', b"Illustrated Children's"), (b'obs', b'Open Bible Stories')])),
                ('paradigm', models.CharField(max_length=2, choices=[(b'P1', b'P1'), (b'P2', b'P2'), (b'P3', b'P3')])),
                ('anticipated_completion_date', models.DateField()),
                ('bible_content', models.ForeignKey(verbose_name=b'Bible Content', to='uw.BibleContent')),
                ('language', models.ForeignKey(to='uw.Language')),
                ('translators', models.ManyToManyField(to='uw.Translator', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='scripture',
            name='wip',
            field=models.ForeignKey(verbose_name=b'Work in Progress', blank=True, to='uw.WorkInProgress', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='language',
            name='networks_translating',
            field=models.ManyToManyField(to='uw.Network', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='country',
            name='primary_networks',
            field=models.ManyToManyField(to='uw.Network', blank=True),
            preserve_default=True,
        ),
    ]
