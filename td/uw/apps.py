from __future__ import absolute_import

from django.apps import AppConfig as BaseAppConfig
from django.utils.importlib import import_module


class AppConfig(BaseAppConfig):

    name = "td.uw"
    verbose_name = "unfoldingWord Metadata"

    def ready(self):
        import_module("td.uw.receivers")
