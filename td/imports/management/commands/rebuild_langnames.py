from django.core.management.base import BaseCommand

from td.tasks import update_langnames_data


class Command(BaseCommand):
    help = "rebuild langnames and langnames_short in the table td_jsondata"

    def handle(self, *args, **options):
        update_langnames_data()
