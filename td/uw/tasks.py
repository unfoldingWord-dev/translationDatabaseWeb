from django.conf import settings
import requests
from eventlog.models import log
from models import Language, Title, Media


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
                for media, _ in medias:
                    resource, created = lang.resources.get_or_create(title=title, media=media)
                    resource.extra_data = row["status"]
                    resource.save()
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
