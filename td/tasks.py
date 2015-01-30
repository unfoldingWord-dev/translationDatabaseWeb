from django.db import connection

from celery import task
from td.imports.models import EthnologueLanguageCode, EthnologueCountryCode
from .models import AdditionalLanguage, Language
from .signals import languages_integrated
from eventlog.models import log


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
       coalesce(cc.id, -1)
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
            language, created = Language.objects.get_or_create(code=r[0])
            language.name = r[1]
            language.country = next(iter(EthnologueCountryCode.objects.filter(pk=int(r[2]))), None)
            language.save()
    languages_integrated.send(sender=Language)
    log(user=None, action="INTEGRATED_SOURCE_DATA", extra={})

