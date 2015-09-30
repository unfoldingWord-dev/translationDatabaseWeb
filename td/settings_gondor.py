import os
import urlparse

import dj_database_url

from .settings import *  # noqa


DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = 2

ALLOWED_HOSTS = [
    os.environ.get("GONDOR_INSTANCE_DOMAIN"),
    "td.unfoldingword.org"
]

DATABASES = {
    "default": dj_database_url.config(),
}

urlparse.uses_netloc.append("redis")
url = urlparse.urlparse(os.environ["REDIS_URL"])
CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "{}:{}".format(url.hostname, url.port),
        "OPTIONS": {
            "DB": 0,
            "PASSWORD": url.password,
        },
    },
}
BROKER_URL = os.environ["REDIS_URL"]  # celery config
CELERY_RESULT_BACKEND = os.environ["REDIS_URL"]  # celery results config

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 2525)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

DEFAULT_HTTP_PROTOCOL = "http"
