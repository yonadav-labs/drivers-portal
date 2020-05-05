import uuid

from django.conf import settings
from django.db import models

from base.models import BaseModel

from payment.fields import StripeDecimalCurrencyAmountField

# Create your models here.
class StripeCharge(BaseModel):
    class Meta:
        verbose_name = "Stripe Charge"
        verbose_name_plural = "Stripe Charges"

    stripe_id = models.CharField(
        max_length=511,
        verbose_name="Stripe ID"
    )
    description = models.TextField(
        verbose_name="Description",
        blank=True
    )
    livemode = models.BooleanField(
        verbose_name="Livemode"
    )
    amount = StripeDecimalCurrencyAmountField(
        verbose_name="Amount"
    )
    paid = models.BooleanField(
        verbose_name="Paid"
    )
    status = models.CharField(
        max_length=511,
        verbose_name="Status"
    )
    source_id = models.CharField(
        max_length=511,
        verbose_name="Source ID",
        blank=True
    )
    source_type = models.CharField(
        max_length=511,
        verbose_name="Source Type"
    )
    customer_id = models.CharField(
        max_length=511,
        verbose_name="Customer ID",
        blank=True
    )
    receipt_url = models.URLField(
        verbose_name="Receipt URL",
        null=True,
        blank=True
    )
    product = models.UUIDField(
        # TODO: Consider a Content type link
        verbose_name="Product paid",
        default=uuid.uuid4,
    )
    user = models.ForeignKey(
        verbose_name="User",
        to=settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "Stripe Charge-{}".format(self.id)

    @property
    def charge_id(self):
        return self.stripe_id

    @property
    def is_paid(self):
        return self.paid and self.status == STRIPE_PAYMENT_CHARGE_SUCCESS


class StripeCustomer(BaseModel):
    class Meta:
        verbose_name = "Stripe Customer"
        verbose_name_plural = "Stripe Customers"

    stripe_id = models.CharField(
        max_length=511,
        verbose_name="Stripe ID"
    )
    livemode = models.BooleanField(
        verbose_name="Livemode"
    )
    last_default_source_id = models.CharField(
        max_length=511,
        verbose_name="Last default source id",
        default=""
    )
    user = models.OneToOneField(
        verbose_name="User",
        to=settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "Stripe Customer-{}".format(self.id)