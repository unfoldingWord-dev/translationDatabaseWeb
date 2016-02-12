from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Checks if the user is a member of a particular group
    :param user: User
    :param group_name: str
    :return: bool
    """
    if not Group.objects.filter(name=group_name).exists():
        return False

    return user.groups.filter(name=group_name).exists()
