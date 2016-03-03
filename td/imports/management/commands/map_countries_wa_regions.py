"""

USAGE:
    python manage.py map_countries_wa_regions < (file).csv

"""

import sys
import csv

from django.core.management.base import BaseCommand

from td.models import Country, WARegion


class Command(BaseCommand):
    help = "Import country-to-WA-region mapping from CSV"
    data = sys.stdin
    country_not_exist = []
    country_ret_multi = []
    wa_region_not_exist = []
    success = 0
    total = 0

    def process_mapping(self, country, wa_region):
        self.total += 1
        c_name = country.decode("utf-8")
        try:
            c = Country.objects.get(name=c_name)
            r = WARegion.objects.get(name=wa_region)
            c.wa_region = r
            c.save()
            self.success += 1
        except Country.DoesNotExist:
            self.country_not_exist.append(country.decode("utf-8"))
        except Country.MultipleObjectsReturned:
            self.country_ret_multi.append(country.decode("utf-8"))
        except WARegion.DoesNotExist:
            self.wa_region_not_exist.append(wa_region)

    def print_summary(self):
        """
        Let user knows the result of import activities
        :return: None
        """
        self.stdout.write(self.style.SUCCESS("======= Summary ======="))
        self.stdout.write(self.style.SUCCESS("%s out of %s record is successfully updated." % (self.success, self.total)))
        if len(self.country_not_exist):
            self.stdout.write(self.style.NOTICE("The following Countries do not exist:"))
            for country in self.country_not_exist:
                self.stdout.write(self.style.NOTICE(" - %s" % country))
        if len(self.country_ret_multi):
            self.stdout.write(self.style.NOTICE("The following Countries returned multiple values:"))
            for country in self.country_ret_multi:
                self.stdout.write(self.style.NOTICE(" - %s" % country))
        if len(self.wa_region_not_exist):
            self.stdout.write(self.style.NOTICE("The following WA Region do not exist:"))
            for wa_region in self.wa_region_not_exist:
                self.stdout.write(self.style.NOTICE(" - %s" % wa_region))

    def handle(self, *args, **options):
        reader = csv.DictReader(self.data)
        for row in reader:
            self.process_mapping(row["country"], row["wa_region"])
        self.print_summary()
