import decimal

from django.conf import settings
from django.db.models import Q

from glom import glom
from stripe import error
from rest_framework import serializers

from payment.constants import (
    STRIPE_PAYMENT_CHARGE_SUCCESS,
    STRIPE_PAYMENT_CHARGE_PENDING,
)
from payment.client import get_stripe_cli, get_plaid_cli
from payment.models import StripeCharge, StripeCustomer


STRIPE_PUBLIC_KEY = getattr(settings, "STRIPE_PUBLIC_KEY", "")
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "")
STRIPE_LIVE_MODE = getattr(settings, "STRIPE_LIVE_MODE")

PLAID_ENV = getattr(settings, "PLAID_ENV")
PLAID_CLIENT_ID = getattr(settings, "PLAID_CLIENT_ID")
PLAID_CLIENT_PUBLIC_KEY = getattr(settings, "PLAID_CLIENT_PUBLIC_KEY")
PLAID_CLIENT_SECRET_KEY = getattr(settings, "PLAID_CLIENT_SECRET_KEY")


def get_stripe_public_key():
    return STRIPE_PUBLIC_KEY


def get_stripe_secret_key():
    return STRIPE_SECRET_KEY


def get_stripe_live_mode():
    return STRIPE_LIVE_MODE


def get_plaid_env():
    return PLAID_ENV


def get_plaid_client_id():
    return PLAID_CLIENT_ID


def get_plaid_public_key():
    return PLAID_CLIENT_PUBLIC_KEY


def get_plaid_secret_key():
    return PLAID_CLIENT_SECRET_KEY


def stripe_amount(amount):
    # A positive integer in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 # noqa
    # https://support.stripe.com/questions/which-zero-decimal-currencies-does-stripe-support
    # https://support.stripe.com/questions/what-is-the-minimum-amount-i-can-charge-with-stripe
    if isinstance(amount, decimal.Decimal):
        return int(amount * 100)
    if isinstance(amount, float):
        return int(amount * 100)
    if isinstance(amount, str):
        return int(decimal.Decimal(amount) * 100)
    return amount * 100


def unstripe_amount(amount):
    return amount / 100


def create_stripe_charge(
    *,
    payment_type,
    amount,
    description,
    email,
    user,
    metadata,
    product,
    customer=None,
    source=None
):
    stripe_charge_data = {
        "currency": "usd",
        "amount": stripe_amount(amount),
        "description": description,
        "receipt_email": email,
        "metadata": metadata,
    }

    if customer:
        stripe_charge_data.update({"customer": customer.stripe_id})

    if source:
        stripe_charge_data.update({"source": source})

    stripe = get_stripe_cli()

    try:
        stripe_charge = stripe.Charge.create(**stripe_charge_data)
    except error.CardError as charge_exception:
        raise serializers.ValidationError(charge_exception.user_message)
    except stripe.error.InvalidRequestError as charge_exception:
        # Invalid parameters were supplied to Stripe's API
        # No such customer
        if (
            charge_exception.code == "resource_missing"
            and charge_exception.param == "customer"
        ):
            raise serializers.ValidationError("Temporary error. Please try again.")
        elif (
            charge_exception.code is None
            and charge_exception.user_message == "This account cannot create payments."
        ):
            # This seems a bug on the plaid + stripe testing  platform
            # Raise a validation error so customer can pay choose
            # to pay with credit card
            raise serializers.ValidationError("Temporary error. Please try again.")
        else:
            raise charge_exception
    except error.StripeError as charge_exception:
        if payment_type == "bank_account":
            raise serializers.ValidationError(charge_exception.user_message)
        raise charge_exception

    source_id = glom(stripe_charge, "source.id", default="")
    source_type = glom(stripe_charge, "source.id", default="payment_type")

    charge_data = {
        "stripe_id": glom(stripe_charge, "id", default=""),
        "description": glom(stripe_charge, "description", default=description),
        "livemode": glom(stripe_charge, "livemode", default=get_stripe_live_mode()),
        "amount": glom(stripe_charge, "amount", default=amount),
        "paid": glom(stripe_charge, "paid", default=False),
        "status": glom(stripe_charge, "status", default=STRIPE_PAYMENT_CHARGE_PENDING),
        "source_id": source_id,
        "source_type": source_type,
        "receipt_url": glom(stripe_charge, "receipt_url", default=""),
        "user": user,
        "product": product,
    }

    charge = StripeCharge(**charge_data)
    charge.save()
    return charge


def create_stripe_customer(
    *, email, description, user, metadata, source, stripe_id=None
):
    # First time customer create it on stripe
    customer_data = {
        "description": description,
        "email": email,
        "metadata": metadata,
        "source": source,
    }
    stripe = get_stripe_cli()
    stripe_customer = stripe.Customer.create(**customer_data)
    default_source = glom(stripe_customer, "default_source", default="")
    customer = StripeCustomer.objects.create(
        **{
            "livemode": get_stripe_live_mode(),
            "stripe_id": stripe_customer.get("id"),
            "user": user,
            "last_default_source_id": default_source,
        }
    )
    return customer


def get_or_create_stripe_customer(
    *, email, description, user, metadata, source, stripe_id=None
):

    try:
        q_params = {"user": user, "livemode": get_stripe_live_mode()}
        if stripe_id:
            q_params.update({"stripe_id": stripe_id})
        customer = StripeCustomer.objects.get(**q_params)
        # Update stripe customer sources
        stripe = get_stripe_cli()
        stripe_customer = stripe.Customer.modify(
            customer.stripe_id, **{"metadata": metadata, "source": source}
        )
        default_source = glom(stripe_customer, "default_source", default="")
        customer.last_default_source_id = default_source
        customer.save()

    except StripeCustomer.DoesNotExist:
        # First time customer create it on stripe
        customer_data = {
            "description": description,
            "email": email,
            "metadata": metadata,
            "source": source,
            "user": user,
        }
        customer = create_stripe_customer(**customer_data)

    return customer


def exchange_plaid_token(*, public_token, account_id):
    plaid = get_plaid_cli()
    exchange_token_response = plaid.Item.public_token.exchange(public_token)
    access_token = exchange_token_response["access_token"]

    stripe_response = plaid.Processor.stripeBankAccountTokenCreate(
        access_token, account_id
    )
    return stripe_response["stripe_bank_account_token"]


def get_quote_process_charge(quote_process_id, user):
    try:
        return StripeCharge.objects.get(user=user, product=quote_process_id)
    except StripeCharge.DoesNotExist:
        return None


def is_quote_process_paid(quote_process_id, user):
    try:
        charge = StripeCharge.objects.get(
            user=user,
            product=quote_process_id,
            paid=True,
            status=STRIPE_PAYMENT_CHARGE_SUCCESS,
        )
        return True
    except StripeCharge.DoesNotExist:
        return False


def is_quote_process_paid_or_pending(quote_process_id, user):
    try:
        charge = StripeCharge.objects.filter(
            Q(status=STRIPE_PAYMENT_CHARGE_SUCCESS)
            | Q(status=STRIPE_PAYMENT_CHARGE_PENDING)
        ).get(user=user, product=quote_process_id)
        return True
    except StripeCharge.DoesNotExist:
        return False
