from django.db import transaction

from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
  RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView,
  UpdateAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User

from quote.models import QuoteProcess
from quote.serializers import (
  RetrieveUpdateQuoteProcessSerializer, CreateQuoteProcessSerializer,
  RetrieveQuoteProcessSerializer, CreateQuoteSoftFalloutSerializer,
  UpdateQuoteProcessOptionsSerializer, UpdateQuoteProcessUserSerializer
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
  queryset = QuoteProcess.objects.without_user()
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
