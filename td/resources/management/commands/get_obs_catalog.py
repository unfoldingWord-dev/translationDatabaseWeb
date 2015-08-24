from django.core.management.base import BaseCommand
from ...tasks import update_obs_resources


class Command(BaseCommand):
    help = "update Open Bible Stories resources from the OBS Catalog API"

    def handle(self, *args, **options):
        update_obs_resources()
