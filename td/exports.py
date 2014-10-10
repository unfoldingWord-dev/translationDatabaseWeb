import json

from django.db import connection

from td.imports.models import SIL_ISO_639_3

from .models import AdditionalLanguage


class Export(object):

    @property
    def additionals(self):
        if not hasattr(self, "_additionals"):
            self._additionals = {
                x.two_letter or x.three_letter or x.ietf_tag: x.native_name or x.common_name
                for x in AdditionalLanguage.objects.all()
            }
        return self._additionals


class LanguageCodesExport(Export):

    def data(self):
        qs = SIL_ISO_639_3.objects.filter(
            scope=SIL_ISO_639_3.SCOPE_INDIVIDUAL,
            language_type=SIL_ISO_639_3.TYPE_LIVING
        )
        codes = [
            x.part_1 or x.code
            for x in qs
        ]
        codes.extend(self.additionals.keys())
        codes.sort()
        return codes

    @property
    def text(self):
        return ", ".join(self.data())


class LanguageNamesExport(Export):

    def data(self):
        cursor = connection.cursor()
        cursor.execute("""
    select coalesce(nullif(x.part_1, ''), x.code) as code,
           coalesce(nullif(nn1.native_name, ''), nullif(nn2.native_name, ''), x.ref_name) as name
      from imports_sil_iso_639_3 x
 left join imports_wikipediaisolanguage nn1 on x.part_1 = nn1.iso_639_1
 left join imports_wikipediaisolanguage nn2 on x.code = nn2.iso_639_3
where x.scope = %s and x.language_type = %s order by code;
""", [SIL_ISO_639_3.SCOPE_INDIVIDUAL, SIL_ISO_639_3.TYPE_LIVING])
        rows = cursor.fetchall()
        rows.extend(self.additionals.items())
        rows.sort()
        return rows

    @property
    def text(self):
        return "\n".join(["{}\t{}".format(r[0], r[1].encode("utf-8")) for r in self.data()])

    @property
    def json(self):
        return json.dumps([
            dict(lc=x[0], ln=x[1])
            for x in self.data()
        ], indent=4)
