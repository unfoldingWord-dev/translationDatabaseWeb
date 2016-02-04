# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-13 20:45
from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations, models, connection
from django.contrib.auth.models import User
import django.db.models.deletion


def migrate_user(apps, schema_editor):
    cursor = connection.cursor()
    cursor.execute("SELECT id, user_account_id FROM gl_tracking_regionaldirector")
    RegionalDirector = apps.get_model("gl_tracking", "RegionalDirector")
    for row in cursor.fetchall():
        try:
            rd = RegionalDirector.objects.get(id=row[0])
            rd.user_id = User.objects.get(id=row[1])
            rd.save()
        except ObjectDoesNotExist:
            print "\n" + unicode(row[1]) + " cannot be found in the list of user. Data not migrated."


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gl_tracking', '0013_remove_regionaldirector_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='regionaldirector',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='regdir', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(migrate_user)
    ]
