# NOTE: Temporary way (using DB and management command) to solve langnames.json problem

from django.core.management.base import BaseCommand

from td.tasks import update_langnames_data


class Command(BaseCommand):
    help = "Update langnames data that will be returned as langnames.json"

    def handle(self, *args, **options):
        update_langnames_data()
