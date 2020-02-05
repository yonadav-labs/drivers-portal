from rest_framework import serializers

from users.models import User

from quote.models import QuoteProcess


class RetrieveQuoteProcessSerializer(serializers.ModelSerializer):

  def validate_email(self, value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError(
          "A user with this email already exists")
    return value

  class Meta:
    fields = (
        'id', 'tlc_number', 'tlc_name', 'vehicle_vin', 'vehicle_owner',
        'license_plate', 'base_name', 'base_number', 'vehicle_year',
        'insurance_carrier_name', 'insurance_policy_number',
        'tlc_license_years', 'dmv_license_years',
        'driver_points_last_months', 'fault_accidents_last_months',
        'defensive_driving_certificate', 'accident_avoidance_system',
        'email',
    )
    read_only_fields = (
        'id', 'tlc_number', 'tlc_name', 'vehicle_vin', 'vehicle_owner',
        'license_plate', 'base_name', 'base_number', 'vehicle_year',
        'insurance_carrier_name', 'insurance_policy_number',
        'tlc_license_years', 'dmv_license_years',
        'driver_points_last_months', 'fault_accidents_last_months',
        'defensive_driving_certificate', 'accident_avoidance_system',
        'email',
    )
    model = QuoteProcess

class RetrieveUpdateQuoteProcessSerializer(serializers.ModelSerializer):

  def validate_email(self, value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError("A user with this email already exists")
    return value

  class Meta:
    fields = (
        'id', 'tlc_number', 'tlc_name', 'vehicle_vin', 'vehicle_owner', 
        'license_plate','base_name', 'base_number', 'vehicle_year', 
        'insurance_carrier_name', 'insurance_policy_number', 
        'tlc_license_years', 'dmv_license_years',
        'driver_points_last_months', 'fault_accidents_last_months',
        'defensive_driving_certificate', 'accident_avoidance_system',
        'email',
    )
    model = QuoteProcess


class CreateQuoteProcessSerializer(serializers.ModelSerializer):

  def validate_email(self, value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError(
          "A user with this email already exists")
    
    if QuoteProcess.objects.filter(email=value):
      raise serializers.ValidationError(
        "A quote process with this email already exists"
      )
    return value

  class Meta:
    fields = (
        'id', 'tlc_number', 'tlc_name', 'vehicle_vin', 'vehicle_owner',
        'license_plate', 'base_name', 'base_number', 'vehicle_year',
        'insurance_carrier_name', 'insurance_policy_number',
        'tlc_license_years', 'dmv_license_years',
        'driver_points_last_months', 'fault_accidents_last_months',
        'defensive_driving_certificate', 'accident_avoidance_system',
        'email',
    )
    model = QuoteProcess
