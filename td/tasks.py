from __future__ import absolute_import

from django.db import connection

from celery import task
from eventlog.models import log

from td.imports.models import EthnologueLanguageCode, EthnologueCountryCode, SIL_ISO_639_3
from td.uw.models import Language, Country

from .models import AdditionalLanguage
from .signals import languages_integrated


@task()
def integrate_imports():
    additionals = {
        x.two_letter or x.three_letter or x.ietf_tag: x.native_name or x.common_name
        for x in AdditionalLanguage.objects.all()
    }
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
       x.id
  from imports_sil_iso_639_3 x
left join imports_ethnologuelanguagecode lc on x.code = lc.code
left join imports_wikipediaisolanguage nn1 on x.part_1 = nn1.iso_639_1
left join imports_wikipediaisolanguage nn2 on x.code = nn2.iso_639_3
left join imports_ethnologuecountrycode cc on lc.country_code = cc.code
 where lc.status = %s or lc.status is NULL order by code;
""", [EthnologueLanguageCode.STATUS_LIVING])
    rows = cursor.fetchall()
    rows.extend([(x[0], x[1], -1) for x in additionals.items()])
    rows.sort()
    for r in rows:
        if r[0] is not None:
            language, _ = Language.objects.get_or_create(code=r[0])
            language.name = r[1]
            if r[1] == r[3]:
                language.source = EthnologueLanguageCode.objects.get(pk=r[4])
            if r[1] == r[5]:
                language.source = EthnologueLanguageCode.objects.get(pk=r[6])
            if r[1] == r[7]:
                language.source = SIL_ISO_639_3.objects.get(pk=r[8])
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
        country.area = ecountry.area
        country.name = ecountry.name
        country.source = ecountry
        country.save()
