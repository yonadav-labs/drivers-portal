from datetime import datetime

from django.db import migrations, models, transaction

from quote.constants import PAYMENT_DAY, PAYMENT_MONTHS
from quote.utils import get_hereford_fee


@transaction.atomic()
def generate_policy_payments(apps, schema_editor):
    Policy = apps.get_model('policy', 'Policy')
    PolicyPayment = apps.get_model('policy', 'PolicyPayment')
    policies = Policy.objects.all()
    for policy in policies:
        quote_payment = policy.quote_process.quoteprocesspayment

        # Deposit
        PolicyPayment.objects.create(
            policy=policy,
            payment_due_date=quote_payment.payment_date,
            payment_date=quote_payment.payment_date,
            payment_amount=quote_payment.deposit_payment_amount,
            fee_amount=0,
            is_deposit=True,
            is_paid=True
        )
        
        # Payments
        payment_months = PAYMENT_MONTHS.get(policy.quote_process.deposit)
        payment_day = PAYMENT_DAY.get(policy.quote_process.deposit)
        payment_year = datetime.today().year
        payment_amount = quote_payment.official_hereford_quote / len(payment_months)
        fee_amount = get_hereford_fee(policy.quote_process.deposit)

        for month in payment_months:
            payment_due_date = datetime(payment_year, month, payment_day)
            PolicyPayment.objects.create(
                policy=policy,
                payment_due_date=payment_due_date,
                payment_amount=payment_amount,
                fee_amount=fee_amount
            )
        
        policy.fee_amount = fee_amount
        policy.save()


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0006_policypayment'),
    ]

    operations = [
        migrations.RunPython(generate_policy_payments, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='policy',
            name='fee_amount',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Fee Amount'),
        ),
    ]
