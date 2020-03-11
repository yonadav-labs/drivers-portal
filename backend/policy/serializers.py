from rest_framework import serializers

from policy.models import Policy, PolicyPayment
from payment.utils import apply_stripe_fee, apply_plaid_fee

class ListPolicySerializer(serializers.ModelSerializer):

  class Meta:
    model = Policy
    fields = (
      'id', 'policy_number'
    )
    read_only_fields = (
        'id', 'policy_number'
    )


class PolicyPaymentSerializer(serializers.ModelSerializer):
  stripe_fee = serializers.SerializerMethodField()
  plaid_fee = serializers.SerializerMethodField()

  def get_stripe_fee(self, obj):
    amount = float(obj.payment_amount)
    return apply_stripe_fee(amount) - amount

  def get_plaid_fee(self, obj):
    amount = float(obj.payment_amount)
    return apply_plaid_fee(amount) - amount

  class Meta:
    model = PolicyPayment
    fields = (
      'id', 'payment_due_date', 'payment_date', 'payment_amount', 'is_deposit',
      'is_paid', 'fee_amount', 'stripe_fee', 'plaid_fee'
    )

class RetrievePolicySerializer(serializers.ModelSerializer):
  tlc_number = serializers.CharField(source="quote_process.tlc_number")
  vehicle_vin = serializers.CharField(source="quote_process.vehicle_vin")
  license_plate = serializers.CharField(source="quote_process.license_plate")
  premium = serializers.SerializerMethodField()
  payments = serializers.SerializerMethodField()

  def get_premium(self, obj):
    return obj.quote_process.quoteprocesspayment.official_hereford_quote

  def get_payments(self, obj):
    return PolicyPaymentSerializer(
      obj.policypayment_set.all().order_by('payment_due_date'),
      many=True
    ).data

  class Meta:
    model = Policy
    fields = (
      'id', 'policy_number', 'certificate_of_liability', 'fh1_document',
      'insurance_document', 'tlc_number', 'vehicle_vin', 'license_plate',
      'premium', 'payments'
    )
    read_only_fields = (
      'id', 'policy_number', 'certificate_of_liability', 'fh1_document',
      'insurance_document', 'tlc_number', 'vehicle_vin', 'license_plate',
    )
