import re

from django.core.cache import cache
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from account.signals import password_changed
from account.signals import user_sign_up_attempt, user_signed_up
from account.signals import user_login_attempt, user_logged_in
from corsheaders.signals import check_request_enabled

from pinax.eventlog.models import log

from .models import Country, Language, LanguageAltName, AdditionalLanguage, TempLanguage, WARegion
from .tasks import reset_langnames_cache, update_alt_names, create_comment_tag, delete_comment_tag, notify_external_apps
from .signals import languages_integrated
from td.resources.tasks import notify_templanguage_created


@receiver(post_save, sender=WARegion)
def handle_wa_region_save(sender, instance=None, created=False, **kwargs):
    "slug" in instance.tracker.changed().keys() and create_comment_tag(instance)


@receiver(post_delete, sender=WARegion)
def handle_wa_region_delete(sender, instance=None, **kwargs):
    instance and delete_comment_tag(instance)


@receiver(post_save, sender=TempLanguage)
def handle_templanguage_save(sender, instance, **kwargs):
    if kwargs["created"]:
        lang = Language.objects.create(
            code=instance.code,
            name=instance.name,
            direction=instance.direction,
            country=instance.country,
        )
        instance.lang_assigned = lang
        instance.save()
        notify_templanguage_created(instance, lang)


@receiver(post_save, sender=AdditionalLanguage)
def handle_additionallanguage_save(sender, instance, **kwargs):
    a_code = instance.merge_code()
    lang, created = Language.objects.get_or_create(code=a_code)
    lang.name = instance.merge_name()
    lang.direction = instance.direction
    lang.iso_639_3 = instance.three_letter
    lang.save()


@receiver(post_delete, sender=AdditionalLanguage)
def handle_additionallanguage_delete(sender, instance, **kwargs):
    d_code = instance.merge_code()
    try:
        lang = Language.objects.get(code=d_code)
        lang.delete()
    except ObjectDoesNotExist:
        pass


@receiver(post_save, sender=Language)
def handle_language_save(sender, instance=None, created=False, **kwargs):
    if instance is not None:
        notify_external_apps("CREATE" if created else "UPDATE", instance)
        if "code" in instance.tracker.changed().keys():
            create_comment_tag(instance)
    reset_langnames_cache.delay()
    cache.set("map_gateway_refresh", True)


@receiver(post_delete, sender=Language)
def handle_language_delete(sender, instance=None, **kwargs):
    if instance is not None:
        # notify_external_apps("DELETE", instance)
        delete_comment_tag(instance)
    reset_langnames_cache.delay()
    cache.set("map_gateway_refresh", True)


@receiver(post_save, sender=LanguageAltName)
def handle_alt_name_save(sender, instance=None, created=False, **kwargs):
    if instance is not None:
        # notify_external_apps("CREATE" if created else "UPDATE", instance)
        update_alt_names(instance.code)


@receiver(post_delete, sender=LanguageAltName)
def handle_alt_name_delete(sender, instance=None, **kwargs):
    if instance is not None:
        # notify_external_apps("DELETE", instance)
        update_alt_names(instance.code)


@receiver(post_save, sender=Country)
def handle_country_save(sender, instance=None, created=False, **kwargs):
    if instance is not None:
        # notify_external_apps("CREATE" if created else "UPDATE", instance)
        "code" in instance.tracker.changed().keys() and create_comment_tag(instance)
    cache.set("map_gateway_refresh", True)


@receiver(post_delete, sender=Country)
def handle_country_delete(sender, instance=None, **kwargs):
    if instance is not None:
        # notify_external_apps("DELETE", instance)
        delete_comment_tag(instance)
    cache.set("map_gateway_refresh", True)


@receiver(languages_integrated)
def handle_languages_integrated(sender, **kwargs):
    reset_langnames_cache.delay()


@receiver(user_logged_in)
def handle_user_logged_in(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="USER_LOGGED_IN",
        extra={}
    )


@receiver(password_changed)
def handle_password_changed(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="PASSWORD_CHANGED",
        extra={}
    )


@receiver(user_login_attempt)
def handle_user_login_attempt(sender, **kwargs):
    log(
        user=None,
        action="LOGIN_ATTEMPTED",
        extra={
            "username": kwargs.get("username"),
            "result": kwargs.get("result")
        }
    )


@receiver(user_sign_up_attempt)
def handle_user_sign_up_attempt(sender, **kwargs):
    log(
        user=None,
        action="SIGNUP_ATTEMPTED",
        extra={
            "username": kwargs.get("username"),
            "email": kwargs.get("email"),
            "result": kwargs.get("result")
        }
    )


@receiver(user_signed_up)
def handle_user_signed_up(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="USER_SIGNED_UP",
        extra={}
    )

@receiver(check_request_enabled)
def cors_allow_all(sender, request, **kwargs):
    """
    Sets Access-Control-Allow-Origin: * for paths defined in the
    `CORS_ALLOW_ALL_ORIGINS_PATH_REGEX_WHITELIST` setting.

    https://github.com/adamchainz/django-cors-headers/tree/f29997e958becf4f1f7b730475e68566b08d62de#signals
    """
    for exemption in settings.CORS_ALLOW_ALL_ORIGINS_PATH_REGEX_WHITELIST:
        if re.match(exemption, request.path):
            return True
    return False
