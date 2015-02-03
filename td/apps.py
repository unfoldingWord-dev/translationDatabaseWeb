from __future__ import absolute_import

from django.apps import AppConfig as BaseAppConfig
from django.conf import settings
from django.utils.importlib import import_module

from celery import Celery


class AppConfig(BaseAppConfig):

    name = "td"
    verbose_name = "Translation Database"

    def ready(self):
        app = Celery("td")
        app.config_from_object("django.conf:settings")
        app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
        import_module("td.receivers")