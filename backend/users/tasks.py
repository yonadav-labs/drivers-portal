from celery.decorators import task

from django.contrib.auth import get_user_model
from django.utils import timezone

from base.emails import send_email

from users.constants import USER_WELCOME_TEMPLATE_ID

from users.models import MagicLink, ResetPasswordLink

USER_MODEL = get_user_model()


@task(name="send_welcome_email_taks")
def send_welcome_email_task(user_id):
    user = USER_MODEL.objects.get(id=user_id)
    # TODO: If user comes from fleet process use for the moment the fleet name
    if user.is_fleet_manager:
        _name = user.fleet.fleet_name
    else:
        _name = user.full_name
    context = {"fullName": _name}
    subject = "Welcome to Stableins."
    send_email(
        receiver=user.email,
        context=context,
        subject=subject,
        template_id=USER_WELCOME_TEMPLATE_ID,
    )


@task(name="delete_expired_links")
def delete_expired_links():
    MagicLink.objects.expired().delete()


@task(name="delete_expired_reset_links")
def delete_expired_reset_links():
    ResetPasswordLink.objects.filter(
        expire_on__lte=timezone.now(),
    ).delete()
