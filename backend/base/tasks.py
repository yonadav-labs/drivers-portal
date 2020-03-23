from django.urls import reverse

from celery.decorators import task

from base.emails import (
    send_admin_notification_documents_submitted_email,
    send_user_welcome_email, send_user_documents_submitted,
    send_user_quote_ready, send_user_reset_password_email
)


@task(name='send_admin_notification_task')
def send_admin_notification_task(user_id):
    from users.models import User, MagicLink
    user = User.objects.get(id=user_id)
    documents_id = user.quoteprocess.quoteprocessdocuments.id
    admin_url = reverse(
        'stable_admin:quote_quoteprocessdocuments_change',  
        args=[documents_id]
      )
    send_admin_notification_documents_submitted_email(user, admin_url)


@task(name='send_user_welcome_task')
def send_user_welcome_task(user_id):
    from users.models import User, MagicLink
    user = User.objects.get(id=user_id)
    ml, _ = MagicLink.objects.get_or_create(user=user, valid_forever=True)
    send_user_welcome_email(user, ml.get_url())


@task(name='send_user_submitted_task')
def send_user_submitted_task(user_id):
    from users.models import User, MagicLink
    user = User.objects.get(id=user_id)
    ml, _ = MagicLink.objects.get_or_create(user=user, valid_forever=True)
    send_user_documents_submitted(user, ml.get_url())


@task(name='send_user_quote_task')
def send_user_quote_task(user_id):
    from users.models import User, MagicLink
    user = User.objects.get(id=user_id)
    ml, _ = MagicLink.objects.get_or_create(user=user, valid_forever=True)
    send_user_quote_ready(user, ml.get_url())


@task(name='send_user_reset_password_task')
def send_user_reset_password_task(link_id):
    from users.models import ResetPasswordLink
    rl = ResetPasswordLink.objects.get(id=link_id)
    send_user_reset_password_email(rl.user, rl.get_url())
