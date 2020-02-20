from rest_framework import serializers

from quote.models import (
  QuoteProcess, QuoteProcessDocuments, QuoteProcessPayment,
  QuoteProcessVariations)

class QuoteProcessVariationsSerializer(serializers.ModelSerializer):

  class Meta:
    fields = (
        'liability_total', 'body_injury', 'property_damage', 'personal_injury_protection',
        'aditional_personal_injury_protection', 'uninsured_motorist', 'physical_total',
        'physical_comprehensive', 'physical_collision',
    )
    model = QuoteProcessVariations

class QuoteProcessSerializer(serializers.ModelSerializer):

  class Meta:
    fields = (
        'id', 'created',
        'tlc_number', 'tlc_name', 'vehicle_vin', 'vehicle_owner', 'license_plate', 'base_name', 'base_number',
        'vehicle_year', 'vehicle_weight', 'is_clean_air_vehicle', 'insurance_carrier_name',
        'insurance_policy_number', 'tlc_license_years', 'dmv_license_years', 'driver_points_last_months',
        'fault_accidents_last_months', 'defensive_driving_certificate', 'accident_avoidance_system',
        'vehicle_owner', 'dash_cam', 'accidents_72_months', 'vehicle_is_hybrid', 'dwi_36_months',
        'fault_accident_pedestrian', 'speeding_violation', 'email', 'quote_amount', 'deposit',
        'deductible', 'start_date', 'status', 'is_hereford',
    )
    model = QuoteProcess


def get_quote_export(quote_process):
  header = QuoteProcessSerializer.Meta.fields + QuoteProcessVariationsSerializer.Meta.fields
  quote_data = QuoteProcessSerializer(quote_process).data
  quote_variations_data = {}
  variations = getattr(quote_process, 'quoteprocessvariations', None)
  if variations:
    quote_variations_data = QuoteProcessVariationsSerializer(
        variations).data
  return (header, {
    **quote_data,
    **quote_variations_data
  })
