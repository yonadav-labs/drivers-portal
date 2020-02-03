from django.core.mail import EmailMessage

from base.constants import DEV_TEST_EMAIL_TEMPLATE_EMAIL_ID


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
