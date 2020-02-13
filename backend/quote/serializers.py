from rest_framework import serializers

from base.tasks import (
  send_admin_notification_task, send_user_submitted_task
)
from importer.models import BaseType
from payment.utils import apply_stripe_fee, apply_plaid_fee
from users.models import User, MagicLink

from quote.models import (
  QuoteProcess, QuoteSoftFallout, QuoteProcessDocuments,
  QuoteProcessDocumentsAccidentReport,
  QuoteProcessPayment)


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
        'deposit' , 'start_date', 'quote_amount', 'deductible',
        'dash_cam', 'accidents_72_months', 'vehicle_is_hybrid', 'dwi_36_months', 
        'fault_accident_pedestrian', 'speeding_violation', 'vehicle_owner'
    )
    read_only_fields = (
        'id', 'tlc_number', 'tlc_name', 'vehicle_vin', 'vehicle_owner',
        'license_plate', 'base_name', 'base_number', 'vehicle_year',
        'insurance_carrier_name', 'insurance_policy_number',
        'tlc_license_years', 'dmv_license_years',
        'driver_points_last_months', 'fault_accidents_last_months',
        'defensive_driving_certificate', 'accident_avoidance_system',
        'email', 'status', 'deposit' , 'start_date', 'quote_amount',
        'deductible', 'dash_cam', 'accidents_72_months', 'vehicle_is_hybrid', 
        'dwi_36_months', 'fault_accident_pedestrian', 'speeding_violation', 
        'vehicle_owner'
    )
    model = QuoteProcess

class RetrieveUpdateQuoteProcessSerializer(serializers.ModelSerializer):

  def validate_email(self, value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError("A user with this email already exists")
    return value

  def update(self, obj, validated_data):
    obj = super().update(obj, validated_data)
    base_type = BaseType.objects.get(base_number=validated_data['base_number'])
    obj.base_type = base_type
    obj.save()
    return obj

  class Meta:
    fields = (
        'id', 'tlc_number', 'tlc_name', 'vehicle_vin', 'vehicle_owner', 
        'license_plate','base_name', 'base_number', 'vehicle_year', 
        'insurance_carrier_name', 'insurance_policy_number', 
        'tlc_license_years', 'dmv_license_years',
        'driver_points_last_months', 'fault_accidents_last_months',
        'defensive_driving_certificate', 'accident_avoidance_system',
        'email', 'dash_cam', 'accidents_72_months', 'vehicle_is_hybrid', 
        'dwi_36_months', 'fault_accident_pedestrian', 'speeding_violation', 
        'vehicle_owner'
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

  def create(self, validated_data):
    base_type = BaseType.objects.get(base_number=validated_data['base_number'])
    return QuoteProcess.objects.create(
      **validated_data,
      base_type=base_type
    )

  class Meta:
    fields = (
        'id', 'tlc_number', 'tlc_name', 'vehicle_vin', 'vehicle_owner',
        'license_plate', 'base_name', 'base_number', 'vehicle_year',
        'insurance_carrier_name', 'insurance_policy_number',
        'tlc_license_years', 'dmv_license_years',
        'driver_points_last_months', 'fault_accidents_last_months',
        'defensive_driving_certificate', 'accident_avoidance_system',
        'email', 'dash_cam', 'accidents_72_months', 'vehicle_is_hybrid', 
        'dwi_36_months', 'fault_accident_pedestrian', 'speeding_violation', 
        'vehicle_owner'
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
      'tlc_license_back_side', 'base_letter', 'proof_of_address', 'defensive_driving_certificate',
      'is_submitted_for_review', 'accident_reports', 'is_broker_of_record_signed',
      'requires_broker_of_record'
    )
    read_only_fields = (
      'id', 'dmv_license_front_side', 'dmv_license_back_side', 'tlc_license_front_side', 
      'tlc_license_back_side', 'base_letter', 'proof_of_address', 'defensive_driving_certificate',
      'is_submitted_for_review', 'accident_reports', 'is_broker_of_record_signed',
      'requires_broker_of_record'
    )
    model = QuoteProcessDocuments

class UpdateQuoteProcessDocumentsFileSerializer(serializers.ModelSerializer):

  class Meta:
    fields = (
      'id', 'dmv_license_front_side', 'dmv_license_back_side', 'tlc_license_front_side', 
      'tlc_license_back_side', 'base_letter', 'proof_of_address', 'defensive_driving_certificate',
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
    if validated_data.get('is_broker_of_record_signed'):
      obj.is_broker_of_record_signed = validated_data.get(
          'is_broker_of_record_signed')
    if validated_data.get('is_submitted_for_review') is True:
      obj.set_is_submitted_for_review()
      send_admin_notification_task.delay(str(obj.quote_process.user.id))
      send_user_submitted_task.delay(str(obj.quote_process.user.id))
    obj.save()
    return obj

  class Meta:
    fields = (
        'id', 'is_submitted_for_review', 'is_broker_of_record_signed'
    )
    read_only_fields = ('id', )
    model = QuoteProcessDocuments


class RetrieveQuoteProcessPaymentSerializer(serializers.ModelSerializer):
  deposit = serializers.SerializerMethodField()
  monthly_payment = serializers.SerializerMethodField()
  hereford_fee = serializers.SerializerMethodField()
  stripe_fee = serializers.SerializerMethodField()
  plaid_fee = serializers.SerializerMethodField()

  def get_deposit(self, obj):
    return obj.get_deposit()

  def get_monthly_payment(self, obj):
    return obj.get_monthly_payment()

  def get_hereford_fee(self, obj):
    return obj.get_hereford_fee()

  def get_stripe_fee(self, obj):
    deposit = obj.get_deposit()
    return apply_stripe_fee(deposit) - deposit

  def get_plaid_fee(self, obj):
    deposit = obj.get_deposit()
    return apply_plaid_fee(deposit) - deposit

  class Meta:
    fields = (
      'id', 'official_hereford_quote', 'liability_amount', 'physical_amount', 'payment_date',
      'deposit', 'monthly_payment', 'hereford_fee', 'stripe_fee', 'plaid_fee'
    )
    read_only_fields = (
      'id', 'official_hereford_quote', 'liability_amount', 'physical_amount', 'payment_date',
      'deposit', 'monthly_payment', 'hereford_fee', 'stripe_fee', 'plaid_fee'
    )
    model = QuoteProcessPayment
