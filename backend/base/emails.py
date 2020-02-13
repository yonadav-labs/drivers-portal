from django.core.mail import EmailMessage
from django.conf import settings

from base.constants import MAIN_TEMPLATE_ID, DEV_TEST_EMAIL_TEMPLATE_EMAIL_ID


def send_dev_test_email(receiver="dummy@test.com", sandbox=True):

    subject = "This is a development test email"
    message = EmailMessage(subject=subject, to=[receiver])

    message.merge_data = {receiver: {"firstName": "Mr.Dummy", "lastName": "Bubbles"}}
    message.template_id = DEV_TEST_EMAIL_TEMPLATE_EMAIL_ID
    message.esp_extra = {"mail_settings": {"sandbox_mode": {"enable": sandbox}}}
    message.send()


def send_email(
    *, receiver, context, subject, template_id, attachments=None, extra=None
):
    message = EmailMessage(subject=subject, to=[receiver])

    message.merge_data = {receiver: {**context}}

    message.template_id = template_id

    message.esp_extra = {
        "mail_settings": {
            "sandbox_mode": {
                "enable": False
            }
        }
    }

    if extra:
        message.esp_extra = {**message.esp_extra, **extra}

    if attachments:
        for attachment in attachments:
            message.attach_file(attachment)

    message.send()


def send_user_welcome_email(user, cta_url):
    return send_email(
        receiver=user.email,
        subject="Welcome to Stable!",
        context={
            "subject": "Welcome to Stable!",
            "title": "Welcome to Stable!",
            "content": (
                "Thank you for creating a quote with us! You are almost done. "
                "Just upload the few documents in your dashboard and well get "
                "your policy going in no time!"
            ),
            "cta": "Go to Stable",
            "cta_url": cta_url
        },
        template_id=MAIN_TEMPLATE_ID
    )


def send_user_documents_submitted(user, cta_url):
    return send_email(
        receiver=user.email,
        subject="Thank you for submitting all of your documents!",
        context={
            "subject": "Thank you for submitting all of your documents!",
            "title": "Thank you for submitting all of your documents!",
            "content": (
                "Stable has kicked off the automated underwriting process. "
                "You will be notified soon when your policy is ready!"
            ),
            "cta": "Go to Stable",
            "cta_url": cta_url
        },
        template_id=MAIN_TEMPLATE_ID
    )


def send_user_quote_ready(user, cta_url):
    return send_email(
        receiver=user.email,
        subject="Your quote has been finalized!",
        context={
            "subject": "Your quote has been finalized!",
            "title": "Your quote has been finalized!",
            "content": (
                "Check out your verified quote and payment details on your dashboard."
            ),
            "cta": "Go to Stable",
            "cta_url": cta_url
        },
        template_id=MAIN_TEMPLATE_ID
    )


def send_admin_notification_documents_submitted_email(user, cta_url):
    return send_email(
        receiver=settings.ADMIN_EMAIL,
        subject="User has submitted all of their documents",
        context={
            "subject": "User has submitted all of their documents!",
            "title": "User has submitted all of their documents!",
            "content": (
                "{} has submitted all of their documents."
            ).format(user.full_name),
            "cta": "Go to Dashboard",
            "cta_url": cta_url
        },
        template_id=MAIN_TEMPLATE_ID
    )
