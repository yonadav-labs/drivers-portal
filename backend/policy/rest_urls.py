from django.urls import path

from policy.rest_views import ListPolicyAPIView, RetrievePolicyAPIView

urlpatterns = [
    path('list/', ListPolicyAPIView.as_view(), name="policy_list"),
    path('retrieve/<uuid:pk>/', RetrievePolicyAPIView.as_view(), name="policy_retrieve"),
]
