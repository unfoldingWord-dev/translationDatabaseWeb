
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.contenttypes.models import ContentType


from .models import (
    BibleContent,
    Country,
    Language,
    Network,
    Organization,
    Resource,
    TranslationNeed,
    Translator,
    Scripture,
    WorkInProgress
)


ENTITIES = [
    BibleContent,
    Country,
    Language,
    Network,
    Organization,
    Resource,
    TranslationNeed,
    Translator,
    Scripture,
    WorkInProgress
]


@receiver(post_save)
def handle_entity_save(sender, instance, *args, **kwargs):
    """
    Entities will have `.source` property set on them during any user change.
    During integration phase, source not being set will allow entity
    saving without causing the recursion here.
    """
    if sender in ENTITIES:
        if getattr(instance, "source", None) is not None:
            for attribute in instance.tracker.changed().keys():
                instance.attributes.create(
                    attribute=attribute,
                    value=getattr(instance, attribute) or "",
                    source_ct=ContentType.objects.get_for_model(instance.source),
                    source_id=instance.source.pk
                )
