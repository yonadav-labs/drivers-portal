from rest_framework import serializers

from users.models import User, MagicLink

from quote.models import (
  QuoteProcess, QuoteSoftFallout, QuoteProcessDocuments,
  QuoteProcessDocumentsAccidentReport)


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
        'email', 'status', 'quoteprocessdocuments', 'quoteprocesspayment',
        'deposit' , 'start_date', 'quote_amount'
    )
    read_only_fields = (
        'id', 'tlc_number', 'tlc_name', 'vehicle_vin', 'vehicle_owner',
        'license_plate', 'base_name', 'base_number', 'vehicle_year',
        'insurance_carrier_name', 'insurance_policy_number',
        'tlc_license_years', 'dmv_license_years',
        'driver_points_last_months', 'fault_accidents_last_months',
        'defensive_driving_certificate', 'accident_avoidance_system',
        'email', 'status', 'deposit' , 'start_date', 'quote_amount'
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


# Quote Process Documents Accident Report

class GetQuoteProcessDocumentsMixin(object):
  
  def _get_quote_process_documents(self):
    request = self.context.get('request')
    if not request:
      raise AttributeError("Request must be added to context")

    try:
      quote_process_documents = request.user.quoteprocess.quoteprocessdocuments
    except (QuoteProcess.DoesNotExists, QuoteProcessDocuments.DoesNotExists) as e:
      raise serializers.ValidationError("This user doesn't have a quote process ready")
    return quote_process_documents


class NestedQuoteProcessAccidentReportSerializer(serializers.ModelSerializer):
  class Meta:
    fields = (
      'id', 'accident_report',
    )
    read_only_fields = (
      'id', 'accident_report',
    )
    model = QuoteProcessDocumentsAccidentReport


class CreateQuoteProcessDocumentsAccidentReportSerializer(
        GetQuoteProcessDocumentsMixin, serializers.ModelSerializer):

  def create(self, validated_data):
    quote_process_documents = self._get_quote_process_documents()

    return self.Meta.model.objects.create(
      quote_process_documents=quote_process_documents,
      **validated_data
    )

  class Meta:
    fields = (
      'id', 'accident_report',
    )
    model = QuoteProcessDocumentsAccidentReport


class UpdateQuoteProcessDocumentsAccidentReportSerializer(serializers.ModelSerializer):

  class Meta:
    fields = (
      'id', 'accident_report'
    )
    model = QuoteProcessDocumentsAccidentReport


# Quote Process Documents
class RetrieveQuoteProcessDocumentsSerializer(serializers.ModelSerializer):
  accident_reports = NestedQuoteProcessAccidentReportSerializer(
    source="quoteprocessdocumentsaccidentreport_set",
    many=True
  )

  class Meta:
    fields = (
      'id', 'dmv_license_front_side', 'dmv_license_back_side', 'tlc_license_front_side', 
      'tlc_license_back_side', 'proof_of_address', 'defensive_driving_certificate',
      'is_submitted_for_review', 'accident_reports'
    )
    read_only_fields = (
      'id', 'dmv_license_front_side', 'dmv_license_back_side', 'tlc_license_front_side', 
      'tlc_license_back_side', 'proof_of_address', 'defensive_driving_certificate',
      'is_submitted_for_review', 'accident_reports'
    )
    model = QuoteProcessDocuments

class UpdateQuoteProcessDocumentsFileSerializer(serializers.ModelSerializer):

  class Meta:
    fields = (
      'id', 'dmv_license_front_side', 'dmv_license_back_side', 'tlc_license_front_side', 
      'tlc_license_back_side', 'proof_of_address', 'defensive_driving_certificate',
    )
    model = QuoteProcessDocuments


class UpdateQuoteProcessDocumentsSerializer(serializers.ModelSerializer):

  def validate(self, validated_data):
    if validated_data.get('is_submitted_for_review') is True:
      obj = QuoteProcessDocuments.objects.get(
        quote_process__user=self.context['request'].user
      )
      if not obj.check_ready_for_review():
        raise serializers.ValidationError({
          "non_field_errors": [
              "Documents are not ready for review", 
          ]
        })
    return validated_data

  def update(self, obj, validated_data):
    if validated_data.get('is_broker_record_signed'):
      obj.is_broker_record_signed = validated_data.get(
          'is_broker_record_signed')
    if validated_data.get('is_submitted_for_review') is True:
      obj.set_is_submitted_for_review()
    obj.save()
    return obj

  class Meta:
    fields = (
        'id', 'is_submitted_for_review', 'is_broker_record_signed'
    )
    read_only_fields = ('id', )
    model = QuoteProcessDocuments
