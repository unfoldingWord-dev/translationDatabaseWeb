import importlib

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "td.uwadmin"

    def ready(self):
        importlib.import_module("td.uwadmin.receivers")
