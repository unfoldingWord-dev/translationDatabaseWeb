"""

USAGE:
    python manage.py language_alt_names (username) < (file).csv

"""

import sys
import csv

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from ....models import Language, LanguageAltName


class Command(BaseCommand):
    help = "Import language alternate names from CSV"
    data = sys.stdin
    user = None
    lang_not_exist = []
    lang_alt_name_exist = 0
    lang_alt_name_created = 0

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

    def process_alt_name(self, code, name):
        """
        Create LanguageAltName and link it to Language
        :param code: ISO-639-3 code
        :param name: Alternate name of a language
        :return: None
        """
        obj, created = LanguageAltName.objects.get_or_create(code=code, name=name.decode("utf-8"))
        if created:
            self.lang_alt_name_created += 1
            # NOTE: Using filter instead of get because there's a possibility that multiple languages share the same
            #    iso-639-3 code. For example: 'pt' and 'pt-br'.
            languages = Language.objects.filter(iso_639_3=code)
            for language in languages:
                language.alt_name = obj
                language.source = self.user
                language.save()
                # NOTE: Even though the obj is saved when it's created, this second manual save is what triggers the
                #    desired update for language.alt_names. Check out handle_alt_name_save() in td/receivers.py
                obj.save()
            if not len(languages):
                self.lang_not_exist.append(code)
        else:
            self.lang_alt_name_exist += 1

    def print_summary(self):
        """
        Let user knows the result of import activities
        :return: None
        """
        self.stdout.write(self.style.SUCCESS("======= Summary ======="))
        if len(self.lang_not_exist):
            self.stdout.write(self.style.NOTICE("The following languages do not exist: %s. LanguageAltName(s) created,"
                                                "but no connection made to Language" % self.lang_not_exist))
        if self.lang_alt_name_exist:
            self.stdout.write(self.style.NOTICE("%s LanguageAltName(s) already exist") % self.lang_alt_name_exist)
        self.stdout.write(self.style.SUCCESS("Import is done. %s LanguageAltName(s) created"
                                             % self.lang_alt_name_created))

    def handle(self, *args, **options):
        try:
            self.user = User.objects.get(username=options["username"][0])
            reader = csv.DictReader(self.data)
            for row in reader:
                self.process_alt_name(row["code"], row["name"])
            self.print_summary()
        except User.DoesNotExist:
            raise CommandError("User with username '%s' doesn't exist" % options["username"][0])
