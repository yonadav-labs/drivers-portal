from rest_framework import serializers

from users.models import User, MagicLink

from quote.models import QuoteProcess, QuoteSoftFallout


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
        'email', 'status', 'quoteprocessdocuments', 'quoteprocesspayment'
    )
    read_only_fields = (
        'id', 'tlc_number', 'tlc_name', 'vehicle_vin', 'vehicle_owner',
        'license_plate', 'base_name', 'base_number', 'vehicle_year',
        'insurance_carrier_name', 'insurance_policy_number',
        'tlc_license_years', 'dmv_license_years',
        'driver_points_last_months', 'fault_accidents_last_months',
        'defensive_driving_certificate', 'accident_avoidance_system',
        'email', 'status', 'quoteprocessdocuments', 'quoteprocesspayment'
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


class UpdateQuoteProcessOptionsSerializer(serializers.ModelSerializer):
      
  class Meta:
    fields = (
      'quote_amount', 'deposit', 'deductible', 'start_date',
    )
    model = QuoteProcess
    read_only_fields = ('quote_amount', )


class UpdateQuoteProcessUserSerializer(serializers.ModelSerializer):
  magic_link = serializers.SerializerMethodField()

  def get_magic_link(self, obj):
    if obj.user:
      magic_link = MagicLink.objects.create(user=obj.user)
      return str(magic_link.id)

  def validate_email(self, value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError(
          "A user with this email already exists")

    return value

  class Meta:
    fields = ('email', 'magic_link')
    model = QuoteProcess

class CreateQuoteSoftFalloutSerializer(serializers.ModelSerializer):

  class Meta:
    fields = (
      'id', 'name', 'phone_number', 'email'
    )
    model = QuoteSoftFallout
