from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from policy.models import Policy
from policy.serializers import (
  ListPolicySerializer, RetrievePolicySerializer
)

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
