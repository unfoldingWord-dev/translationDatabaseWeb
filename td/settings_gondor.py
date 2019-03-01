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

if "REDIS_URL" in os.environ:
    REDIS_URL = os.environ["REDIS_URL"]
    parsed_redis_url = urlparse.urlparse(REDIS_URL)
    CACHES = {
        "default": {
            "BACKEND": "redis_cache.RedisCache",
            "LOCATION": "%s:%s" % (parsed_redis_url.hostname, parsed_redis_url.port),
            "OPTIONS": {
                "DB": 0
            },
        },
    }
    if parsed_redis_url.password is not None:
        CACHES["default"]["OPTIONS"]["PASSWORD"] = parsed_redis_url.password
    BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 2525)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

DEFAULT_HTTP_PROTOCOL = "http"
