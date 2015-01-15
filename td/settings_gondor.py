import os
import urlparse

import dj_database_url

from .settings import *  # noqa


DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = 2

ALLOWED_HOSTS = [
    "vd725.gondor.co",
    "td.unfoldingword.org"
]

DATABASES = {
    "default": dj_database_url.config(env="GONDOR_DATABASE_URL"),
}

if "GONDOR_REDIS_URL" in os.environ:
    urlparse.uses_netloc.append("redis")
    url = urlparse.urlparse(os.environ["GONDOR_REDIS_URL"])
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


MEDIA_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "media")
STATIC_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "static")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

DEFAULT_HTTP_PROTOCOL = "http"
