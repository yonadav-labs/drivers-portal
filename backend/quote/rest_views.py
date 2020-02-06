from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from quote.models import QuoteProcess
from quote.serializers import (
  RetrieveUpdateQuoteProcessSerializer, CreateQuoteProcessSerializer,
  RetrieveQuoteProcessSerializer, CreateQuoteSoftFalloutSerializer
)

class CreateQuoteProcessView(CreateAPIView):
  permission_classes = (AllowAny, )
  serializer_class = CreateQuoteProcessSerializer

class RetrieveUpdateQuoteProcessView(RetrieveUpdateAPIView):
  lookup_field = "email"
  queryset = QuoteProcess.objects.filter(user__isnull=True)
  permission_classes = (AllowAny, )
  serializer_class = RetrieveUpdateQuoteProcessSerializer


class RetrieveQuoteProcessView(RetrieveAPIView):
  queryset = QuoteProcess.objects.filter(user__isnull=True)
  permission_classes = (AllowAny, )
  serializer_class = RetrieveQuoteProcessSerializer


class CreateQuoteSoftFalloutView(CreateAPIView):
  permission_classes = (AllowAny, )
  serializer_class = CreateQuoteSoftFalloutSerializer
