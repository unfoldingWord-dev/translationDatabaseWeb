from __future__ import absolute_import

import importlib

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "td.uw"
    verbose_name = "unfoldingWord Metadata"

    def ready(self):
        importlib.import_module("td.uw.receivers")
