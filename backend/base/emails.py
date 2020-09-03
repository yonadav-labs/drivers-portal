from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import Group

from base.constants import MAIN_TEMPLATE_ID, DEV_TEST_EMAIL_TEMPLATE_EMAIL_ID
from quote.utils import get_quote_info


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


def send_notification(id, quote_process, attachments=[]):
    subject = f"{quote_process.tlc_number}"
    to_email = 'stable.notification@gmail.com'

    body = (
        f"Notification {id}\n\n"
        f"TLC number: {quote_process.tlc_number}\n"
        f"VIN: {quote_process.vehicle_vin}\n"
        f"Name: {quote_process.tlc_name}\n"
        f"Name on Registration: {quote_process.tlc_name}\n"
        f"Email Address: {quote_process.email}\n"
        f"Policy Number: {quote_process.insurance_policy_number}\n"
        f"Insurance Company: {quote_process.insurance_carrier_name}\n"
        f"Base Number and Name: {quote_process.base_number} - {quote_process.base_name}\n\n"
        f"Dash Cam: {'Yes' if quote_process.dash_cam else 'No'}\n"
    )

    if id != 1:
        quote_info = get_quote_info(quote_process)
        body += f"Start Date: {quote_info['start_date']}\n"
        body += f"Annualized Premium: {quote_info['annualized_premium']}\n"
        body += f"ProRated Premium: {quote_info['prorated_premium']}\n"
        body += f"Deposit Amount: {quote_process.deposit}% and {quote_info['deposit_amount']}\n"
        body += f"Monthly Payment 1: {quote_info['monthly_payment1_date']} - {quote_info['monthly_payment1_amount']}+{quote_info['hereford_fee']}\n"
        body += f"Monthly Payment 2: {quote_info['monthly_payment2_date']} - {quote_info['monthly_payment2_amount']}+{quote_info['hereford_fee']}\n"
        body += f"Monthly Payment 3: {quote_info['monthly_payment3_date']} - {quote_info['monthly_payment3_amount']}+{quote_info['hereford_fee']}\n"

        if quote_process.quoteprocessdocuments.phone:
            body += f"Phone Number: {quote_process.quoteprocessdocuments.phone}"

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

    for attachment in attachments:
        message.attach_file(attachment)

    message.send()
