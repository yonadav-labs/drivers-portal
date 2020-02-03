from django.core.management.base import BaseCommand

from base.tasks import send_dev_test_email_task


class Command(BaseCommand):

    help = "Sends a development test email"

    def add_arguments(self, parser):
        parser.add_argument("receiver", type=str, help="Send email to")
        parser.add_argument(
            "-s",
            "--sandbox",
            action="store_true",
            help="Use sandbox mode (email is not sent)",
        )

    def handle(self, *args, **options):
        receiver = options["receiver"]
        sandbox = options["sandbox"]
        send_dev_test_email_task.delay(receiver, sandbox)
        self.stdout.write("Done")
