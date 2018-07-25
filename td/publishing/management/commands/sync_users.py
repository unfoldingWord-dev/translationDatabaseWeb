import codecs

from django.core.management.base import BaseCommand

from ...models import Contact


class Command(BaseCommand):

    def handle(self, *args, **options):
        # login:passwordhash:Real Name:email:groups,comma,seperated
        door43_users = "/var/www/vhosts/door43.org/httpdocs/conf/users.auth.php"
        if len(args) == 1:
            door43_users = args[0]
        with codecs.open(door43_users, encoding="utf-8", mode="r") as fp:
            for line in fp.readlines():
                if line and line[0] in ["#", "\n"]:
                    continue
                parts = line.split(":")
                if parts[0] == "":
                    continue
                obj, created = Contact.objects.get_or_create(
                    d43username=parts[0],
                    defaults={
                        "name": parts[2],
                        "email": parts[3],
                        "other": "Door43 Groups: {}".format(parts[4])
                    }
                )
                if created:
                    print("Created {}".format(obj.name))
