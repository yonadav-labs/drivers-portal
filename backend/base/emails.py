from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import Group

from base.constants import MAIN_TEMPLATE_ID, DEV_TEST_EMAIL_TEMPLATE_EMAIL_ID


def send_dev_test_email(receiver="dummy@test.com", sandbox=True):

    subject = "This is a development test email"
    receiver = receiver if isinstance(receiver, list) else [receiver, ]
    message = EmailMessage(subject=subject, to=receiver)

    message.merge_data = {receiver[0]: {"firstName": "Mr.Dummy", "lastName": "Bubbles"}}
    message.template_id = DEV_TEST_EMAIL_TEMPLATE_EMAIL_ID
    message.esp_extra = {"mail_settings": {"sandbox_mode": {"enable": sandbox}}}
    message.send()


def send_email(
    *, receiver, context, subject, template_id, attachments=None, extra=None
):

    receiver = receiver if isinstance(receiver, list) else [receiver, ]
    message = EmailMessage(subject=subject, to=receiver)
    message.merge_data = {}

    for r in receiver:
        message.merge_data[r] = {**context}

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
    emails = Group.objects.get(name="admin_emails").user_set.values_list('email', flat=True)
    return send_email(
        receiver=emails,
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


def send_user_reset_password_email(user, cta_url):
    return send_email(
        receiver=user.email,
        subject="Reset your password",
        context={
            "subject": "Reset your password",
            "title": "Forgot your password?",
            "content": (
                "We've received a request to recover your password. If it's you who "
                "has made this request, please use the following link to reset your "
                "password. If it wasn't you, don't mind this email."
            ),
            "cta": "Reset your password",
            "cta_url": cta_url
        },
        template_id=MAIN_TEMPLATE_ID
    )


def send_notification(id, data):
    subject = f"{data.tlc_number} - Notification {id}"
    to_email = 'notification@stableins.com'
    to_email = 'it.corridor051@gmail.com'

    body = (
        f"TLC number: {data.tlc_number}\n"
        f"VIN: {data.vehicle_vin}\n"
        f"Name: {data.tlc_name}\n"
        f"Name on Registration: {data.tlc_name}\n"
        f"Email Address: {data.email}\n"
        f"Policy Number: {data.insurance_policy_number}\n"
        f"Insurance Company: {data.insurance_carrier_name}\n"
        f"Base Number and Name: {data.base_number} - {data.base_name}"
    )

    message = EmailMessage(
        subject=subject,
        body=body,
        to=[to_email],
    )

    message.esp_extra = {
        "mail_settings": {
            "sandbox_mode": {
                "enable": False
            }
        }
    }

    message.send()
