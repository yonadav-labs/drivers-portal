import os

from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

from base.models import BaseModel
from quote.models import QuoteProcess
from quote.constants import PAYMENT_DAY, PAYMENT_MONTHS
from quote.utils import get_hereford_fee
from payment.models import StripeCharge


def policy_document_upload_to(instance, filename):
    return os.path.join("policy", instance.user.email, filename)


class Policy(BaseModel):
    user = models.ForeignKey(
        verbose_name="User", to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    quote_process = models.OneToOneField(
        verbose_name="Quote Process",
        to=QuoteProcess,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    policy_number = models.CharField(verbose_name="Policy Number", max_length=255)

    certificate_of_liability = models.FileField(
        verbose_name="Certificate of Liability", upload_to=policy_document_upload_to
    )

    fh1_document = models.FileField(
        verbose_name="FH1 Document", upload_to=policy_document_upload_to
    )

    insurance_document = models.FileField(
        verbose_name="Insurance Document", upload_to=policy_document_upload_to
    )

    fee_amount = models.DecimalField(
        verbose_name="Fee Amount", max_digits=7, decimal_places=2
    )

    autopay = models.BooleanField(verbose_name="Autopay", default=False)

    def _generate_policy_payments(self):
        quote_payment = self.quote_process.quoteprocesspayment
        deposit = quote_payment.deposit_payment_amount

        # Deposit
        PolicyPayment.objects.create(
            policy=self,
            payment_due_date=quote_payment.payment_date,
            payment_date=quote_payment.payment_date,
            payment_amount=deposit,
            fee_amount=0,
            is_deposit=True,
            is_paid=True,
        )

        # Payments
        payment_months = PAYMENT_MONTHS.get(self.quote_process.deposit)
        payment_day = PAYMENT_DAY.get(self.quote_process.deposit)
        payment_year = datetime.today().year
        if len(payment_months) > 0:
            total_premium = quote_payment.official_hereford_quote
            payment_amount = (total_premium - deposit) / len(payment_months)
        fee_amount = get_hereford_fee(self.quote_process.deposit)

        for month in payment_months:
            payment_due_date = datetime(payment_year, month, payment_day)
            PolicyPayment.objects.create(
                policy=self,
                payment_due_date=payment_due_date,
                payment_amount=payment_amount,
                fee_amount=fee_amount,
            )

        self.fee_amount = fee_amount
        self.save()

    def save(self, *args, **kwargs):
        created = self._state.adding is True
        super().save(*args, **kwargs)
        if created:
            self.quote_process.update_status()
            self._generate_policy_payments()

    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __str__(self):
        return (
            f"Policy {self.policy_number} for user "
            f"{self.user.get_full_name()} ({self.user.email})"
        )


class PolicyPayment(BaseModel):
    policy = models.ForeignKey(
        verbose_name="Policy", to=Policy, on_delete=models.CASCADE
    )

    payment_due_date = models.DateField(
        verbose_name="Payment Due Date", null=True, blank=True
    )

    payment_date = models.DateTimeField(
        verbose_name="Payment Date", null=True, blank=True
    )

    payment_amount = models.DecimalField(
        verbose_name="Payment Amount", max_digits=7, decimal_places=2
    )

    fee_amount = models.DecimalField(
        verbose_name="Fee Amount",
        help_text="Change this if you want to change the fee amount for all the unpaid payments.",
        max_digits=7,
        decimal_places=2,
    )

    is_deposit = models.BooleanField(verbose_name="Is Deposit", default=False)

    is_paid = models.BooleanField(verbose_name="Is Paid", default=False)

    stripe_charge = models.OneToOneField(
        verbose_name="Stripe Charge",
        to=StripeCharge,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Policy Payment"
        verbose_name_plural = "Policy Payments"
        ordering = [
            "payment_due_date",
        ]

    def __str__(self):
        return (
            f"Policy {self.policy.policy_number} Payment due "
            f"for {self.payment_due_date}"
        )

    def mark_as_paid(self, charge):
        self.stripe_charge = charge
        self.payment_date = timezone.now()
        self.is_paid = True
        self.save()
