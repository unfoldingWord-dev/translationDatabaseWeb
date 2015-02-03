from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "delete old Wycliffe tables in the database"

    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute("""
            drop table wycliffe_biblecontent cascade;
            drop table wycliffe_country cascade;
            drop table wycliffe_country_primary_networks cascade;
            drop table wycliffe_language cascade;
            drop table wycliffe_language_networks_translating cascade;
            drop table wycliffe_network cascade;
            drop table wycliffe_organization cascade;
            drop table wycliffe_resource cascade;
            drop table wycliffe_scripture cascade;
            drop table wycliffe_translationneed cascade;
            drop table wycliffe_translator cascade;
            drop table wycliffe_translator_languages cascade;
            drop table wycliffe_workinprogress cascade;
            drop table wycliffe_workinprogress_translators cascade;
        """)



