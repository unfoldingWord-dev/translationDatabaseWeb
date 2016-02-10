from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User


class Command(BaseCommand):

    def handle(self, *args, **options):

        # get or create the Publishing auth group
        if Group.objects.filter(name='Publishing').exists():
            print '* The Publishing group already exists.'
            publishing_group = Group.objects.get(name='Publishing')
        else:
            print '* Creating the Publishing group.'
            publishing_group = Group.objects.create(name='Publishing')

        # add the initial users
        self.add_existing_user_to_group(publishing_group, 'jesse')
        # noinspection SpellCheckingInspection
        self.add_existing_user_to_group(publishing_group, 'pjoakes')
        # noinspection SpellCheckingInspection
        self.add_existing_user_to_group(publishing_group, 'ben_jore')
        self.add_existing_user_to_group(publishing_group, 'phil')

    @staticmethod
    def add_existing_user_to_group(group, user_name):

        if not User.objects.filter(username=user_name).exists():
            print '* The user ' + user_name + ' was not found.'
            return

        User.objects.get(username=user_name).groups.add(group)
        print '* Successfully added ' + user_name + ' to the Publishing group.'
