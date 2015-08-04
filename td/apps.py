from __future__ import absolute_import

import importlib

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "td"
    verbose_name = "Translation Database"

    def ready(self):
        importlib.import_module("td.celery")
        importlib.import_module("td.receivers")
