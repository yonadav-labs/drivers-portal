from django.shortcuts import get_object_or_404
from rest_framework.generics import (
  ListAPIView, RetrieveAPIView, CreateAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from policy.models import Policy, PolicyPayment
from policy.serializers import (
  ListPolicySerializer, RetrievePolicySerializer,
  PolicyPaymentSerializer
)
from payment.serializers import (
  StripeChargeCreateSerializer,
  PlaidChargeCreateSerializer
)
from payment.utils import apply_stripe_fee, apply_plaid_fee


class ListPolicyAPIView(ListAPIView):
  permission_classes = (IsAuthenticated, )
  serializer_class = ListPolicySerializer

  def get_queryset(self):
    return self.request.user.policy_set.all()


class RetrievePolicyAPIView(RetrieveAPIView):
  permission_classes = (IsAuthenticated, )
  serializer_class = RetrievePolicySerializer

  def get_queryset(self):
    return self.request.user.policy_set.all()


class PayPolicyPaymentBaseView(CreateAPIView):
  permission_classes = (IsAuthenticated, )

  def _get_amount(self, quote_process_payment):
    raise NotImplementedError("_get_amount must be implemented")

  def create(self, request, *args, **kwargs):
    payment = get_object_or_404(PolicyPayment.objects, 
      id=kwargs['pk']
    )
    data = {
      **request.data,
      'amount': self._get_amount(payment),
      'email': payment.policy.user.email
    }
    serializer = self.serializer_class(
      data=data, 
      context={
        'request': request, 
        'concept': "Policy #{} Payment".format(
          payment.policy.policy_number
        ),
        'product': str(payment.policy.quote_process.id)
      })
    serializer.is_valid(raise_exception=True)
    charge = serializer.save()
    payment.mark_as_paid(charge)
    return Response({
      'id': str(payment.id),
      'payment_date': payment.payment_date
    }, status=status.HTTP_201_CREATED)
  

class PayStripePolicyPaymentView(PayPolicyPaymentBaseView):
  serializer_class = StripeChargeCreateSerializer

  def _get_amount(self, payment):
    return apply_stripe_fee(payment.payment_amount)
    

class PayPlaidPolicyPaymentView(PayPolicyPaymentBaseView):
  serializer_class = PlaidChargeCreateSerializer

  def _get_amount(self, payment):
    return apply_plaid_fee(payment.payment_amount)
