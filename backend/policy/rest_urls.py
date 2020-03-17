from django.urls import path

from policy.rest_views import (
    ListPolicyAPIView, RetrievePolicyAPIView,
    PayStripePolicyPaymentView,
    PayPlaidPolicyPaymentView
)

urlpatterns = [
    path(
        'list/',
        ListPolicyAPIView.as_view(),
        name="policy_list"
    ),
    path(
        'retrieve/<uuid:pk>/',
        RetrievePolicyAPIView.as_view(),
        name="policy_retrieve"
    ),
    path(
        'payment/<uuid:pk>/pay/stripe/',
        PayStripePolicyPaymentView.as_view(),
        name="payment_pay_stripe"
    ),
    path(
        'payment/<uuid:pk>/pay/plaid/',
        PayPlaidPolicyPaymentView.as_view(),
        name="payment_pay_plaid"
    ),
]
