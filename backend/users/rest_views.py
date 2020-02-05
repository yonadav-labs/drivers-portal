from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers

from users.models import User
from users.serializers import RetrieveUserExistsSerializer


class RetrieveUserExistsView(RetrieveUpdateAPIView):
  allowed_methods = ('GET', )
  lookup_field = 'email'
  permission_classes = (AllowAny, )
  queryset = User.objects.all()
  serializer_class = RetrieveUserExistsSerializer
