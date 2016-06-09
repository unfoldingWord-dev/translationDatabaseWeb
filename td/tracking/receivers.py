from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from td.tasks import create_comment_tag, delete_comment_tag
from td.tracking.models import Charter, Event


@receiver(post_save, sender=Charter)
def handle_charter_save(sender, instance=None, created=False, **kwargs):
    "language_id" in instance.tracker.changed().keys() and create_comment_tag(instance)


@receiver(post_delete, sender=Charter)
def handle_charter_delete(sender, instance=None, **kwargs):
    instance and delete_comment_tag(instance)


@receiver(post_save, sender=Event)
def handle_event_save(sender, instance=None, created=False, **kwargs):
    # NOTE: This works on creating a new event and SHOULD work on editing said event's charter. It cannot be confirmed
    # right now because the EventForm.clean_charter is returning the wrong charter, thus not updating the charter info.
    # In other words, the update event form is broken.
    #
    # See github issue #598
    # https://github.com/unfoldingWord-dev/translationDatabaseWeb/issues/598
    changed_keys = instance.tracker.changed().keys()
    ("charter_id" in changed_keys or "number" in changed_keys) and create_comment_tag(instance)


@receiver(post_delete, sender=Event)
def handle_event_delete(sender, instance=None, **kwargs):
    instance and delete_comment_tag(instance)
