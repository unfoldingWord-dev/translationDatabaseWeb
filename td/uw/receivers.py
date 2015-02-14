
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Country


@receiver(post_save, sender=Country)
def handle_country_save(sender, instance, *args, **kwargs):
    print instance.tracker.changed()
