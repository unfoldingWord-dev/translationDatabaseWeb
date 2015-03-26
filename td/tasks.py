from __future__ import absolute_import

from django.db import connection

from celery import task
from eventlog.models import log

from td.imports.models import (
    EthnologueLanguageCode,
    EthnologueCountryCode,
    SIL_ISO_639_3,
    WikipediaISOLanguage,
    IMBPeopleGroup
)

from td.uw.models import Language, Country, Region, Title, Resource, Media

from .models import AdditionalLanguage
from .signals import languages_integrated


@task()
def integrate_imports():
    cursor = connection.cursor()
    cursor.execute("""
select coalesce(nullif(x.part_1, ''), x.code) as code,
       coalesce(nullif(nn1.native_name, ''), nullif(nn2.native_name, ''), x.ref_name) as name,
       coalesce(cc.code, ''),
       nullif(nn1.native_name, '') as nn1name,
       nn1.id,
       nullif(nn2.native_name, '') as nn2name,
       nn2.id,
       x.ref_name as xname,
       x.id,
       x.code as iso_639_3
  from imports_sil_iso_639_3 x
left join imports_ethnologuelanguagecode lc on x.code = lc.code
left join imports_wikipediaisolanguage nn1 on x.part_1 = nn1.iso_639_1
left join imports_wikipediaisolanguage nn2 on x.code = nn2.iso_639_3
left join imports_ethnologuecountrycode cc on lc.country_code = cc.code
 where lc.status = %s or lc.status is NULL order by code;
""", [EthnologueLanguageCode.STATUS_LIVING])
    rows = cursor.fetchall()
    rows.extend([(x.merge_code(), x.merge_name(), None, "", None, "", None, "!ADDL", x.id, x.three_letter) for x in AdditionalLanguage.objects.all()])
    rows.sort()
    for r in rows:
        if r[0] is not None:
            language, _ = Language.objects.get_or_create(code=r[0])
            language.name = r[1]
            if r[1] == r[3]:
                language.source = WikipediaISOLanguage.objects.get(pk=r[4])
            if r[1] == r[5]:
                language.source = WikipediaISOLanguage.objects.get(pk=r[6])
            if r[1] == r[7]:
                language.source = SIL_ISO_639_3.objects.get(pk=r[8])
            if r[7] == "!ADDL":
                language.source = AdditionalLanguage.objects.get(pk=r[8])
            if r[9] != "":
                language.iso_639_3 = r[9]
            language.save()
            if r[2]:
                language.country = next(iter(Country.objects.filter(code=r[2])), None)
                language.source = EthnologueCountryCode.objects.get(code=r[2])
                language.save()
    languages_integrated.send(sender=Language)
    log(user=None, action="INTEGRATED_SOURCE_DATA", extra={})


@task()
def update_countries_from_imports():
    for ecountry in EthnologueCountryCode.objects.all():
        country, _ = Country.objects.get_or_create(code=ecountry.code)
        country.region = next(iter(Region.objects.filter(name=ecountry.area)), None)
        country.name = ecountry.name
        country.source = ecountry
        country.save()


def _get_or_create_object(model, slug, name):
    o, c = model.objects.get_or_create(slug=slug)
    if c:
        o.name = name
        o.save()
    return o


@task()
def integrate_imb_language_data():
    imb_map = {
        "bible_stories": ("onestory-bible-stories", "OneStory Bible Storires", "audio", "Audio"),
        "jesus_film": ("jesus-film", "The Jesus Film", "video", "Video"),
        "gospel_recording": ("gospel-recording-grn", "Gospel Recording (GRN)", "audio", "Audio"),
        "radio_broadcast": ("radio-broadcast-twr-febc", "Radio Broadcast (TWR/FEBC)", "audo", "Audio"),
        "written_scripture": ("bible-portions", "Bible (Portions)", "print", "Print")
    }
    for imb in IMBPeopleGroup.objects.order_by("language").distinct("language"):
        language = next(iter(Language.objects.filter(iso_639_3=imb.rol)), None)
        if not language:
            language = next(iter(Language.objects.filter(code=imb.rol)), None)
        if language:
            for k in imb_map.keys():
                if getattr(imb, k):
                    title = _get_or_create_object(Title, imb_map[k][0], imb_map[k][1])
                    media = _get_or_create_object(Media, imb_map[k][2], imb_map[k][3])
                    resource, _ = Resource.objects.get_or_create(language=language, title=title, media=media)
                    resource.published_flag = True
                    resource.save()
