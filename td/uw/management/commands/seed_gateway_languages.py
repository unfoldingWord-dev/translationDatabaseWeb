from django.core.management.base import BaseCommand
from ...tasks import seed_languages_gateway_language


class Command(BaseCommand):
    help = "assign a gateway_language for languages that don't have one based on associated country"

    def handle(self, *args, **options):
        seed_languages_gateway_language()
