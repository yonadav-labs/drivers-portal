from rest_framework import serializers

from policy.models import Policy

class ListPolicySerializer(serializers.ModelSerializer):

  class Meta:
    model = Policy
    fields = (
      'id', 'policy_number'
    )
    read_only_fields = (
        'id', 'policy_number'
    )

class RetrievePolicySerializer(serializers.ModelSerializer):
  tlc_number = serializers.CharField(source="quote_process.tlc_number")
  vehicle_vin = serializers.CharField(source="quote_process.vehicle_vin")
  license_plate = serializers.CharField(source="quote_process.license_plate")

  class Meta:
    model = Policy
    fields = (
      'id', 'policy_number', 'certificate_of_liability', 'fh1_document',
      'insurance_document', 'tlc_number', 'vehicle_vin', 'license_plate',
    )
    read_only_fields = (
        'id', 'policy_number', 'certificate_of_liability', 'fh1_document',
        'insurance_document', 'tlc_number', 'vehicle_vin', 'license_plate',
    )
