import requests

from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string

from celery import task
from pinax.eventlog.models import log

from .models import Title, Media
from td.models import Country, Language


def _get_obs_api_data():
    r = requests.get(settings.UWADMIN_OBS_API_URL)
    return r


def _clean_json_data(response):
    try:
        return response.json()
    except ValueError:
        return None


def _process_obs_response(response):
    if response.status_code != 200 or _clean_json_data(response) is None:
        log(
            user=None,
            action="GET_OBS_CATALOG_FAILED",
            extra={"status_code": response.status_code, "text": response.content}
        )
    else:
        title, _ = Title.objects.get_or_create(slug="open-bible-stories", defaults={"name": "Open Bible Stories"})
        medias = (Media.objects.get_or_create(slug="print", defaults={"name": "Print"}),
                  Media.objects.get_or_create(slug="mobile", defaults={"name": "Mobile"}))
        record_count = resources_created = resources_updated = 0
        for row in response.json():
            lang = next(iter(Language.objects.filter(code=row["language"])), None)
            if lang:
                resource, created = lang.resources.get_or_create(title=title)
                resource.extra_data = row["status"]
                resource.save()
                for media, _ in medias:
                    resource.medias.add(media)
                if created:
                    resources_created += 1
                else:
                    resources_updated += 1
            record_count += 1
        log(
            user=None,
            action="GET_OBS_CATALOG_SUCCEEDED",
            extra={"records_processed": record_count, "resources_created": resources_created, "resources_updated": resources_updated}
        )
    return response.json()


def update_obs_resources():
    _process_obs_response(_get_obs_api_data())


def seed_languages_gateway_language():
    for lang in Language.objects.filter(gateway_language=None, gateway_flag=False):
        if lang.country and lang.country.gateway_language():
            lang.gateway_language = lang.country.gateway_language()
            lang.save()


def update_map_gateways():
    country_gateways = {
        country.alpha_3_code: {
            "fillKey": country.gateway_language().code if country.gateway_language() else "defaultFill",
            "url": reverse("country_detail", args=[country.pk]),
            "country_code": country.code,
            "gateway_language": country.gateway_language().name if country.gateway_language() else "",
            "gateway_languages": [unicode("({0}) {1}").format(ogl.code, ogl.name) for ogl in country.gateway_languages()]
        }
        for country in Country.objects.all()
    }
    cache.set("map_gateways", country_gateways)
    log(user=None, action="UPDATE_MAP_GATEWAYS")


def get_map_gateways():
    mg = cache.get("map_gateways", None)
    if not mg:
        update_map_gateways()
        mg = cache.get("map_gateways", {})
    return mg


@task()
def check_map_gateways():
    if cache.get("map_gateways_refresh", True):
        cache.set("map_gateways_refresh", False)
        update_map_gateways()


def notify_templanguage_created(templanguage, language):
    plain_content = render_to_string("resources/email/templanguage_notify_plain.html",
                                     {"object": templanguage, "language": language})
    send_mail("Temporary Language #{0}".format(str(templanguage.pk)),
              plain_content,
              settings.EMAIL_FROM,
              settings.TEMPLANGUAGE_NOTIFY_LIST)