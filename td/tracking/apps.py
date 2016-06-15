from __future__ import absolute_import

import importlib

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "td.tracking"

    def ready(self):
        importlib.import_module("td.tracking.receivers")
