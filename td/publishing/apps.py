import importlib

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "td.publishing"

    def ready(self):
        importlib.import_module("td.publishing.receivers")
