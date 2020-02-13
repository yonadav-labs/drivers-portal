from celery.decorators import task

from base.emails import (
    send_admin_notification_documents_submitted_email,
    send_user_welcome_email, send_user_documents_submitted,
    send_user_policy_ready
)
from users.models import User


@task(name='send_admin_notification_task')
def send_admin_notification_task(user_id, cta_url):
    user = User.objects.get(id=user_id)
    send_admin_notification_documents_submitted_email(user, cta_url)


@task(name='send_user_welcome_task')
def send_user_welcome_task(user_id, cta_url):
    user = User.objects.get(id=user_id)
    send_user_welcome_email(user)


@task(name='send_user_submitted_task')
def send_user_submitted_task(user_id, cta_url):
    user = User.objects.get(id=user_id)
    send_user_documents_submitted(user, cta_url)


@task(name='send_user_policy_task')
def send_user_policy_task(user_id, cta_url):
    user = User.objects.get(id=user_id)
    send_user_policy_ready(user, cta_url)
