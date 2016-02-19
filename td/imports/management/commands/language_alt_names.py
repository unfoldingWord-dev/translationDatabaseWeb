"""

USAGE:
    python manage.py language_alt_names <username> < <file>.csv

"""

import sys
import traceback

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from ....models import Language, LanguageAltName


class Command(BaseCommand):
    help = "Import language alternate names from CSV"
    data = sys.stdin.read()
    user = None
    code = None
    name = None

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

    @staticmethod
    def split_endings(data):
        """
        Split string based on CRLF or LF ending
        :param data: Raw strings that may contain line endings
        :return: Array of strings
        """
        return data.split("\r\n") if "\r\n" in data else data.split("\n")

    def process_header(self, r):
        """
        Get column location from header
        :param r:
        :return:
        """
        try:
            self.code = r.index("code")
            self.name = r.index("name")
        except ValueError:
            traceback.print_exc()
            raise CommandError("Failed in identifying fields in columns")

    def process_entry(self, r, i):
        """
        Create LanguageAltName and link it to Language
        :param r: An array of values representing a single row of entry in CSV
        :param i: Row number of the current entry in CSV
        :return: None
        """
        try:
            obj, created = LanguageAltName.objects.get_or_create(code=r[self.code], name=r[self.name].decode("utf-8"))
            if created:
                # NOTE: Filter instead of get because there's a possibility that multiple languages share the same
                #    iso-639-3 code
                languages = Language.objects.filter(iso_639_3=r[self.code])
                for language in languages:
                    language.alt_name = obj
                    language.source = self.user
                    language.save()
                    # NOTE: Even though the obj is saved when it's created, this second manual save is what triggers the
                    #    right update for language.alt_names
                    obj.save()
                if len(languages) <= 0:
                    self.stdout.write(self.style.NOTICE("Language '%s' doesn't exist" % r[self.code]))
            else:
                self.stdout.write(self.style.WARNING("LanguageAltName with code '%s' and name '%s' already exists" %
                                                     (r[self.code], r[self.name].decode("utf-8"))))
        except IndexError:
            self.stdout.write(self.style.WARNING("No code or name in this row. Skipping row %s" % i))
            traceback.print_exc()

    def handle(self, *args, **options):
        try:
            self.user = User.objects.get(username=options["username"][0])
            rows = self.split_endings(self.data)
            for i in range(len(rows)):
                r = rows[i].split(',')
                self.process_header(r) if i == 0 else self.process_entry(r, i)
        except User.DoesNotExist:
            raise CommandError("User with username '%s' doesn't exist" % options["username"][0])
