from django.core.management.base import BaseCommand

import requests

from ... import models
from td.tasks import update_countries_from_imports, integrate_imports


class Command(BaseCommand):
    help = "reload all imports"

    def handle(self, *args, **options):
        session = requests.Session()
        for obj in models.__dict__.values():
            if hasattr(obj, "reload") and callable(obj.reload):
                print("Loading {} records".format(obj._meta.verbose_name))
                obj.reload(session)
        update_countries_from_imports()
        integrate_imports()
