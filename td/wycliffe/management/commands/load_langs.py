from django.core.management.base import BaseCommand

from td.models import Language as SourceLanguage

from ... import models


class Command(BaseCommand):
    help = "populate languages for countries based on Ethnologue"

    def handle(self, *args, **options):
        for country in models.Country.objects.all():
            print country.country.code
            for lang in SourceLanguage.objects.filter(country=country.country):
                print "\t{}: {}".format(lang.code, lang.name.encode("utf-8"))
                _, created = models.Language.objects.get_or_create(country=country, living_language=lang)
                if created:
                    print "\t\tCREATED"
