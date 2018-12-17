import os
import urlparse

import dj_database_url

from .settings import *  # noqa


DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = int(os.environ.get("SITE_ID", "2"))

ALLOWED_HOSTS = [
    "translation-database.herokuapp.com",
    "td.unfoldingword.org",
    "td-demo.unfoldingword.org"
]

DATABASES = {
    "default": dj_database_url.config(),
}

urlparse.uses_netloc.append("redis")
url = urlparse.urlparse(os.environ["REDIS_URL"])
port = 6379 if url.port is None else url.port
CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "{}:{}".format(url.hostname, port),
        "OPTIONS": {
            "DB": 0
        },
    },
}
BROKER_URL = os.environ["REDIS_URL"]  # celery config
CELERY_RESULT_BACKEND = os.environ["REDIS_URL"]  # celery results config

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 2525)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

DEFAULT_HTTP_PROTOCOL = "http"
