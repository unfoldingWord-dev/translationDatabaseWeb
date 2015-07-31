from django.apps import AppConfig as BaseAppConfig
from django.utils.importlib import import_module


class AppConfig(BaseAppConfig):

    name = "td.uwadmin"

    def ready(self):
        import_module("td.uwadmin.receivers")
