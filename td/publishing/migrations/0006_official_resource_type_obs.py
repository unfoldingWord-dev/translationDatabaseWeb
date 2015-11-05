# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_official_resource_types(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    OfficialResourceType = apps.get_model("publishing", "OfficialResourceType")
    OfficialResourceType.objects.create(
        short_name="obs",
        long_name="OpenBibleStory",
        description=(
            "A visual mini-Bible in any language, in text, audio, and video"
            " formats."
        )
    )
    OfficialResourceType.objects.create(
        short_name="ta",
        long_name="translationAcademy",
        description=(
            "A modular, media-based, self-paced trainig course for "
            "translators and translation facilitators."
        )
    )


class Migration(migrations.Migration):

    dependencies = [
        ("publishing", "0005_chapter_frame"),
    ]

    operations = [
        migrations.RunPython(add_official_resource_types),
        migrations.AlterField(
            model_name='officialresource',
            name='resource_type',
            field=models.ForeignKey(
                verbose_name=b'Official resource type',
                to='publishing.OfficialResourceType'
            ),
        ),
        migrations.AlterField(
            model_name='publishrequest',
            name='resource_type',
            field=models.ForeignKey(
                verbose_name=b'Official resource type',
                to='publishing.OfficialResourceType',
                null=True
            ),
        ),
        migrations.AlterField(
            model_name='frame',
            name='identifier',
            field=models.CharField(max_length=50),
        ),
    ]
