from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
  RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView,
  UpdateAPIView, DestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from payment.serializers import (
  StripeDepositChargeCreateSerializer,
  PlaidDepositChargeCreateSerializer
)
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
from quote.utils import generate_variations

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
    return Response(generate_variations(obj))

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
  allowed_methods = ['OPTIONS', 'PUT', 'PATCH', ]
  permission_classes = (IsAuthenticated, )
  serializer_class = UpdateQuoteProcessDocumentsFileSerializer

  def get_object(self):
    return get_object_or_404(
      QuoteProcessDocuments.objects,
      quote_process__user=self.request.user 
    )


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
  
  def perform_create(self, serializer):
    payment = get_object_or_404(QuoteProcessPayment.objects.get(
      quote_process__user=self.request.user,
      payment_date__isnull=True 
    ))
    charge = serializer.save()
    payment.mark_as_paid(charge)


class StripePayQuoteProcessPaymentView(PayQuoteProcessPaymentBaseView):
  serializer_class = StripeDepositChargeCreateSerializer

class PlaidPayQuoteProcessPaymentView(PayQuoteProcessPaymentBaseView):
  serializer_class = PlaidDepositChargeCreateSerializer