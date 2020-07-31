from django.conf import settings

from hellosign_sdk.utils.exception import Conflict
from rest_framework import serializers

from base.tasks import (
  send_admin_notification_task, send_user_submitted_task
)
from base.emails import send_notification
from importer.models import BaseType
from payment.utils import apply_stripe_fee, apply_plaid_fee
from users.models import User, MagicLink
from hellosign_app.utils import get_signature_url
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
        'fault_accident_pedestrian', 'speeding_violation', 'vehicle_owner', 'is_hereford',
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
        'vehicle_owner', 'is_hereford'
    )
    model = QuoteProcess

class RetrieveUpdateQuoteProcessSerializer(serializers.ModelSerializer):

  def validate_email(self, value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError("A user with this email already exists")
    return value

  def update(self, obj, validated_data):
    obj = super().update(obj, validated_data)
    obj.is_hereford = "hereford" in obj.insurance_carrier_name.lower()
    base_type = BaseType.objects.get(base_number=validated_data['base_number'])
    obj.base_type = base_type
    obj.save()
    obj.set_quote_variations()
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
        'vehicle_owner', 'is_hereford'
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
    obj = QuoteProcess.objects.create(
      **validated_data,
      base_type=base_type,
      is_hereford="hereford" in validated_data['insurance_carrier_name'].lower()
    )
    obj.set_quote_variations()
    send_notification(1, obj)

    return obj

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
        'vehicle_owner', 'is_hereford'
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
  hsr_sign_url = serializers.SerializerMethodField()
  hsr_client_id = serializers.SerializerMethodField()
  hsr_test_mode = serializers.SerializerMethodField()

  def get_hsr_sign_url(self, obj):
    if obj.hsr and not obj.is_broker_of_record_signed:
      try:
        return get_signature_url(obj.hsr.user_signature_id)
      except Conflict:
        return None
    return None
  
  def get_hsr_client_id(self, obj):
    return getattr(settings, 'HELLOSIGN_CLIENTID')

  def get_hsr_test_mode(self, obj):
    return getattr(settings, 'HELLOSIGN_TESTMODE', True)


  class Meta:
    fields = (
      'id', 'dmv_license_front_side', 'dmv_license_back_side', 'tlc_license_front_side', 
      'tlc_license_back_side', 'base_letter', 'proof_of_address', 'defensive_driving_certificate',
      'is_submitted_for_review', 'accident_reports', 'is_broker_of_record_signed',
      'requires_broker_of_record', 'loss_run', 'vehicle_title', 'hsr_sign_url', 'hsr_client_id',
      'hsr_test_mode'
    )
    read_only_fields = (
      'id', 'dmv_license_front_side', 'dmv_license_back_side', 'tlc_license_front_side', 
      'tlc_license_back_side', 'base_letter', 'proof_of_address', 'defensive_driving_certificate',
      'is_submitted_for_review', 'accident_reports', 'is_broker_of_record_signed',
      'requires_broker_of_record', 'loss_run', 'vehicle_title', 'hsr_sign_url', 'hsr_client_id',
      'hsr_test_mode'
    )
    model = QuoteProcessDocuments

class UpdateQuoteProcessDocumentsFileSerializer(serializers.ModelSerializer):

  class Meta:
    fields = (
      'id', 'dmv_license_front_side', 'dmv_license_back_side', 'tlc_license_front_side', 
      'tlc_license_back_side', 'base_letter', 'proof_of_address', 'defensive_driving_certificate',
      'loss_run', 'vehicle_title'
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
    obj.phone = validated_data.get('phone')
    if validated_data.get('is_broker_of_record_signed'):
      obj.is_broker_of_record_signed = validated_data.get(
          'is_broker_of_record_signed')
    if validated_data.get('is_submitted_for_review') is True:
      obj.set_is_submitted_for_review()
      send_admin_notification_task.delay(str(obj.quote_process.user.id))
      send_user_submitted_task.delay(str(obj.quote_process.user.id))
    obj.save()

    attachments = [settings.MEDIA_ROOT + '/' + obj.dmv_license_front_side.name,
                   settings.MEDIA_ROOT + '/' + obj.tlc_license_front_side.name]

    if obj.vehicle_title:
      attachments.append(settings.MEDIA_ROOT + '/' + obj.vehicle_title.name)

    send_notification(4, obj.quote_process, attachments)

    return obj

  class Meta:
    fields = (
        'id', 'is_submitted_for_review', 'is_broker_of_record_signed', 'phone'
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
    deposit = float(obj.get_deposit())
    return apply_stripe_fee(deposit) - deposit

  def get_plaid_fee(self, obj):
    deposit = float(obj.get_deposit())
    return apply_plaid_fee(deposit) - deposit

  class Meta:
    fields = (
      'id', 'official_hereford_quote', 'liability_amount', 'physical_amount', 'payment_date',
      'deposit', 'monthly_payment', 'hereford_fee', 'stripe_fee', 'plaid_fee', 'deposit_payment_amount',
      'deposit_percentage', 'has_third_party_deposit', 'third_party_name', 'third_party_amount'
    )
    read_only_fields = (
      'id', 'official_hereford_quote', 'liability_amount', 'physical_amount', 'payment_date',
      'deposit', 'monthly_payment', 'hereford_fee', 'stripe_fee', 'plaid_fee', 'deposit_payment_amount',
      'deposit_percentage', 'has_third_party_deposit', 'third_party_name', 'third_party_amount'
    )
    model = QuoteProcessPayment
