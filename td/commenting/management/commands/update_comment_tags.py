from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from td.models import WARegion, Country, Language
from td.tracking.models import Charter, Event
from td.commenting.models import CommentTag


class Command(BaseCommand):

    def handle(self, *args, **options):
        errors = []
        models = [WARegion, Country, Language, Charter, Event]

        for model in models:
            for instance in model.objects.all():
                try:
                    CommentTag.objects.get_or_create(name=instance.tag_slug, slug=instance.tag_slug,
                                                     content_type=ContentType.objects.get_for_model(instance),
                                                     object_id=instance.id)
                except Exception as e:
                    errors.append(e)

        if len(errors):
            self.stdout.write(self.style.WARNING("The following error(s) occurred when trying to update CommentTag:"))
            for message in errors:
                self.stdout.write(self.style.ERROR(message))
        else:
            self.stdout.write(self.style.SUCCESS("CommentTag is successfully updated"))
