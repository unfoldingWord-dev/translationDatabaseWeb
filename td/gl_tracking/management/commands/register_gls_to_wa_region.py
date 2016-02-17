from django.core.management.base import BaseCommand

from td.models import Language, WARegion


class Command(BaseCommand):
    help = "Register gateway languages to WA Region for administrative purposes"
    mapping = {
        "americas": ["en", "es", "es-419", "pt", "pt-br"],

        "eurasia": ["ar", "ar-x-dcv", "ru", "tr", "fa", "ps", "ur", "ur-x-dcv",
                    "ur-Deva"],

        "africa": ["fr", "sw", "am", "ha"],

        "southasia": ["bn", "ne", "hi", "hi-x-dcv", "gu", "pa", "or", "as",
                      "mr", "kn", "ta", "te", "ml"],

        "pacific": ["id", "id-x-dcv", "pmy", "abs", "xmm", "lew", "sda", "bjn",
                    "mgl", "mkn", "tpi", "pis", "bi", "tet"],

        "asia": ["mn", "zh", "my", "th", "lo", "km", "vi", "ms", "ms-x-dcv",
                 "tl", "ceb"],
    }

    def handle(self, *args, **options):
        errors = []

        # Go through the mapping and register each languages to the wa-region
        for region_slug, codes in self.mapping.iteritems():
            try:
                region = WARegion.objects.get(slug=region_slug)
                for code in codes:
                    try:
                        language = Language.objects.get(code=code)
                        if hasattr(language, "wa_region"):
                            language.wa_region = region
                            language.save()
                        else:
                            errors.append(
                                "Language '" + code + "' has no wa_region attr."
                            )
                    except Language.DoesNotExist:
                        errors.append(
                            "Language with code: '" + code + "' doesn't exist"
                        )
            except WARegion.DoesNotExist:
                errors.append(
                    "WARegion with slug: '" + region_slug + "' doesn't exist"
                )

        # Status message printed based on the existence of error
        if len(errors) > 0:
            self.stdout.write(self.style.WARNING(
                "Gateway Languages are linked, but with the following errors:"
            ))
            for message in errors:
                self.stdout.write(self.style.ERROR("   - " + message))
        else:
            self.stdout.write(self.style.SUCCESS(
                "Gateway Languages are succesfully linked to WA-Regions"
            ))
