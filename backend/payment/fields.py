import decimal

from django.db import models


class StripeDecimalCurrencyAmountField(models.DecimalField):
    """
    A field used to define currency according to djstripe logic.
    Stripe is always in cents. djstripe stores everything in dollars.
    """

    def __init__(self, *args, **kwargs):
        """Assign default args to this field."""
        defaults = {"decimal_places": 2, "max_digits": 8}
        defaults.update(kwargs)
        super().__init__(*args, **defaults)

    def stripe_to_db(self, data):
        """Convert the raw value to decimal representation."""
        val = data.get(self.name)

        # Note: 0 is a possible return value, which is 'falseish'
        if val is not None:
            return val / decimal.Decimal("100")
