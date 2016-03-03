from django.core.management.base import BaseCommand

from td.models import Language


class Command(BaseCommand):
    help = "Fill in language.wa_region with language.country.wa_region"

    def handle(self, *args, **options):
        no_wa_region = []

        for language in Language.objects.all():
            if language.wa_region is None and language.country is not None and language.country.wa_region is not None:
                language.wa_region = language.country.wa_region
                language.save()
            else:
                no_wa_region.append(language.ang or language.ln)

        if len(no_wa_region):
            self.stdout.write(self.style.NOTICE("The following languages have no WA region from country:"))
            for lang in no_wa_region:
                self.stdout.write(self.style.NOTICE(" - %s") % lang.decode("utf-8"))
