from celery.decorators import task

from base.emails import send_dev_test_email


@task(name='send_dev_test_email_task')
def send_dev_test_email_task(receiver, sandbox):
    send_dev_test_email(receiver, sandbox)