from django.core.management import BaseCommand

from td.models import Language, Country


class Command(BaseCommand):

    def handle(self, *args, **options):
        count = 0
        language_codes = [l.code if len(l.code) > 2 else l.iso_639_3 for l in Language.objects.all()]
        country_codes = list(Country.objects.values_list("code", flat=True))

        for cc in country_codes:
            cc = cc.lower()

            try:
                language_codes.index(cc)
                print cc
                count += 1
            except ValueError:
                pass

        print "%d duplicate(s) found\n" % count

        if len(language_codes) != len(set(language_codes)):
            print "internal duplicate(s) found"
            mapping = {}
            for lc in language_codes:
                mapping[lc] = mapping.get(lc, 0) + 1
            for lc in mapping:
                if mapping[lc] > 1:
                    print "%s: %dx" % (lc, mapping[lc])
            print "\n"

        empty_iso_languages = [l for l in Language.objects.all() if (len(l.code) <= 2 and l.iso_639_3 == " ")]
        # for l in empty_iso_languages:
        #     print l
        print empty_iso_languages
        print "\n"
