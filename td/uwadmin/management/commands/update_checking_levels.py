from django.core.management.base import BaseCommand

from ...models import LangCode


class Command(BaseCommand):

    def handle(self, *args, **options):
        LangCode.update_checking_levels()
