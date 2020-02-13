import os

from django.conf import settings
from django.db import models

from base.models import BaseModel
from quote.models import QuoteProcess


def policy_document_upload_to(instance, filename):
    return os.path.join(
        'policy', instance.user.email, filename)

class Policy(BaseModel):
    user = models.ForeignKey(
        verbose_name="User",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    quote_process = models.OneToOneField(
        verbose_name="Quote Process",
        to=QuoteProcess,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    policy_number = models.CharField(
        verbose_name="Policy Number",
        max_length=255
    )

    certifcate_of_liability = models.FileField(
        verbose_name="Certificate of Liability",
        upload_to=policy_document_upload_to
    )

    fh1_document = models.FileField(
        verbose_name="FH1 Document",
        upload_to=policy_document_upload_to
    )

    insurance_document = models.FileField(
        verbose_name="Insurance Document",
        upload_to=policy_document_upload_to
    )

    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __str__(self):
        return (
            f"Policy {self.policy_number} for user "
            f"{self.user.get_full_name()} ({self.user.email})"
        )
