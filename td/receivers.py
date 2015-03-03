from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from account.signals import password_changed
from account.signals import user_sign_up_attempt, user_signed_up
from account.signals import user_login_attempt, user_logged_in

from eventlog.models import log

from .models import AdditionalLanguage
from td.uw.models import Language
from .signals import languages_integrated
from .tasks import integrate_imports


@receiver(post_save, sender=AdditionalLanguage)
def handle_additionallanguage_save(sender, **kwargs):
    pass
    # we don't need to call integrate_imports.delay()
    # for a single language add
    # todo: create a new task that adds the new AdditionalLanguage to Language

@receiver(post_delete, sender=AdditionalLanguage)
def handle_additionallanguage_delete(sender, instance, **kwargs):
    d_code = instance.merge_code()
    try:
        lang = Language.objects.get(code=d_code)
        lang.delete()
    except ObjectDoesNotExist:
        pass


@receiver(post_save, sender=Language)
def handle_language_save(sender, **kwargs):
    cache.delete("langnames")


@receiver(post_delete, sender=Language)
def handle_language_delete(sender, **kwargs):
    cache.delete("langnames")


@receiver(languages_integrated)
def handle_languages_integrated(sender, **kwargs):
    cache.delete("langnames")
    cache.set("langnames", Language.names_data(), None)


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
