import stripe
from plaid import Client


def get_stripe_cli():
    from payment.utils import get_stripe_secret_key

    stripe.api_key = get_stripe_secret_key()
    return stripe


def get_plaid_cli():
    from payment.utils import (
        get_plaid_client_id,
        get_plaid_secret_key,
        get_plaid_env,
        get_plaid_public_key,
    )

    return Client(
        client_id=get_plaid_client_id(),
        secret=get_plaid_secret_key(),
        environment=get_plaid_env(),
        public_key=get_plaid_public_key(),
    )
