import logging
from errno import errorcode
import os

from ...celery import app

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Check if celery is up and running."

    def handle(self, *args, **options):
        try:
            inspector = app.control.inspect()
            result = inspector.stats()
            if not result:
                return logging.critical("No running Celery workers were found.")
        except IOError as e:
            msg = "Error connecting to the backend: {0}.".format(str(e))
            if len(e.args) > 0 and errorcode.get(e.args[0]) == "ECONNREFUSED":
                msg += " Check that the Redis server is running."
            return logging.critical(msg)

        active = inspector.active()
        kind = os.environ.get("GONDOR_INSTANCE_KIND")
        if kind == "primary" and "celery@celery-i2249-s4963" not in active.keys():
            return logging.critical("celery@celery-i2249-s4963 is not running")
        print("Celery is up and running.")
