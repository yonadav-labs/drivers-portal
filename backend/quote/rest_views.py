from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
  RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView,
  UpdateAPIView, DestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from base.tasks import send_user_welcome_task
from base.emails import send_notification
from payment.serializers import (
  StripeChargeCreateSerializer,
  PlaidChargeCreateSerializer
)
from payment.utils import apply_plaid_fee, apply_stripe_fee
from users.models import User

from quote.models import (
  QuoteProcess, QuoteProcessDocuments, QuoteProcessDocumentsAccidentReport,
  QuoteProcessPayment)
from quote.serializers import (
  RetrieveUpdateQuoteProcessSerializer, CreateQuoteProcessSerializer,
  RetrieveQuoteProcessSerializer, CreateQuoteSoftFalloutSerializer,
  UpdateQuoteProcessOptionsSerializer, UpdateQuoteProcessUserSerializer,
  UpdateQuoteProcessDocumentsFileSerializer, 
  CreateQuoteProcessDocumentsAccidentReportSerializer,
  UpdateQuoteProcessDocumentsAccidentReportSerializer,
  RetrieveQuoteProcessDocumentsSerializer, UpdateQuoteProcessDocumentsSerializer, 
  RetrieveQuoteProcessPaymentSerializer
)
from quote.quote_calc import get_quote_variations

class CreateQuoteProcessView(CreateAPIView):
  permission_classes = (AllowAny, )
  serializer_class = CreateQuoteProcessSerializer


class RetrieveUpdateQuoteProcessView(RetrieveUpdateAPIView):
  lookup_field = "email"
  queryset = QuoteProcess.objects.without_user()
  permission_classes = (AllowAny, )
  serializer_class = RetrieveUpdateQuoteProcessSerializer


class RetrieveCalcQuoteProcessVariationsView(RetrieveAPIView):
  queryset = QuoteProcess.objects.without_user()
  permission_classes = (AllowAny, )
  
  def retrieve(self, request, *args, **kwargs):
    obj = self.get_object()
    return Response(get_quote_variations(obj))

class RetrieveQuoteProcessView(RetrieveAPIView):
  queryset = QuoteProcess.objects.all()
  permission_classes = (AllowAny, )
  serializer_class = RetrieveQuoteProcessSerializer


class UpdateQuoteProcessOptionsView(UpdateAPIView):
  queryset = QuoteProcess.objects.without_user()
  permission_classes = (AllowAny, )
  serializer_class = UpdateQuoteProcessOptionsSerializer

  def perform_update(self, serializer):
    instance = serializer.save()
    instance.set_quote_variations()
    

class UpdateQuoteProcessUserView(UpdateAPIView):
  queryset = QuoteProcess.objects.without_user()
  permission_classes = (AllowAny, )
  serializer_class = UpdateQuoteProcessUserSerializer

  def get_object(self):
    obj = super().get_object()
    if not obj.is_ready_for_user and obj.variations:
      raise ValidationError({
        'non_field_errors': [
          "Quote Process needs a deposit and a start date before having a user"
        ]
      })
    return obj

  def perform_update(self, serializer):
    with transaction.atomic():
      obj = serializer.save()
      user = User.objects.create_passwordless_user(obj.email)
      obj.add_user(user)
    send_user_welcome_task.delay(str(user.id))
    

class CreateQuoteSoftFalloutView(CreateAPIView):
  permission_classes = (AllowAny, )
  serializer_class = CreateQuoteSoftFalloutSerializer


# Quote Process Documents


class RetrieveQuoteProcessDocumentsView(RetrieveAPIView):
  permission_classes = (IsAuthenticated, )
  serializer_class = RetrieveQuoteProcessDocumentsSerializer

  def get_object(self):
    return QuoteProcessDocuments.objects.get(
      quote_process__user=self.request.user
    )

class UpdateQuoteProcessDocumentsFileView(UpdateAPIView):
  permission_classes = (IsAuthenticated, )
  serializer_class = UpdateQuoteProcessDocumentsFileSerializer

  def get_object(self):
    return get_object_or_404(
      QuoteProcessDocuments.objects,
      quote_process__user=self.request.user 
    )

  def perform_update(self, serializer):    
    instance = serializer.save()

    if 'dmv_license_front_side' in self.request.data:
      nid = '3.1'
    elif 'tlc_license_front_side' in self.request.data:
      nid = '3.2'
    else:
      nid = '3.3'

    send_notification(nid, instance.quote_process)


class UpdateQuoteProcessDocumentsView(UpdateAPIView):
  permission_classes = (IsAuthenticated, )
  serializer_class = UpdateQuoteProcessDocumentsSerializer

  def get_object(self):
    return get_object_or_404(
        QuoteProcessDocuments.objects,
        quote_process__user=self.request.user
    )


# Quote Process Documents Accident Reports
class CreateQuoteProcessDocumentsAccidentReportView(CreateAPIView):
  permission_classes = (IsAuthenticated, )
  serializer_class = CreateQuoteProcessDocumentsAccidentReportSerializer

class UpdateQuoteProcessDocumentsAccidentReportView(UpdateAPIView):
  permission_classes = (IsAuthenticated, )
  serializer_class = UpdateQuoteProcessDocumentsAccidentReportSerializer

  def get_queryset(self):
    return QuoteProcessDocumentsAccidentReport.objects.filter(
      quote_process_documents__quote_process__user=self.request.user
    )

class DeleteQuoteProcessDocumentsAccidentReportView(DestroyAPIView):
  permission_classes = (IsAuthenticated, )
  serializer_class = CreateQuoteProcessDocumentsAccidentReportSerializer

  def get_queryset(self):
    return QuoteProcessDocumentsAccidentReport.objects.filter(
      quote_process_documents__quote_process__user=self.request.user
    )

# Quote Process Payment
class RetrieveQuoteProcessPaymentView(RetrieveAPIView):
  permission_classes = (IsAuthenticated, )
  serializer_class = RetrieveQuoteProcessPaymentSerializer

  def get_object(self):
    return QuoteProcessPayment.objects.get(
      quote_process__user=self.request.user
    )


class PayQuoteProcessPaymentBaseView(CreateAPIView):
  permission_classes = (IsAuthenticated, )

  def _get_amount(self, quote_process_payment):
    raise NotImplementedError("_get_amount must be implemented")

  def create(self, request, *args, **kwargs):
    payment = get_object_or_404(QuoteProcessPayment.objects, 
      quote_process__user=self.request.user,
      payment_date__isnull=True 
    )
    data = {
      **request.data,
      'amount': self._get_amount(payment),
      'email': payment.quote_process.email
    }
    serializer = self.serializer_class(
      data=data, 
      context={
        'request': request, 
        'concept': str(payment.quote_process),
        'product': str(payment.quote_process.id)
      })
    serializer.is_valid(raise_exception=True)
    charge = serializer.save()
    payment.mark_as_paid(charge)
    return Response({
      'id': str(payment.id),
      'payment_date': payment.payment_date
    }, status=status.HTTP_201_CREATED)
  

class StripePayQuoteProcessPaymentView(PayQuoteProcessPaymentBaseView):
  serializer_class = StripeChargeCreateSerializer

  def _get_amount(self, payment):
    deposit = payment.deposit_payment_amount
    if payment.third_party_amount:
      deposit = payment.deposit_payment_amount - payment.third_party_amount
    return apply_stripe_fee(deposit)
    

class PlaidPayQuoteProcessPaymentView(PayQuoteProcessPaymentBaseView):
  serializer_class = PlaidChargeCreateSerializer

  def _get_amount(self, payment):
    deposit = payment.deposit_payment_amount
    if payment.third_party_amount:
      deposit = payment.deposit_payment_amount - payment.third_party_amount
    return apply_plaid_fee(deposit)
    