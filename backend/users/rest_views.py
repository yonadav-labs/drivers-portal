from django.conf import settings

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
  RetrieveAPIView, UpdateAPIView, CreateAPIView,
  RetrieveUpdateAPIView
)
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
  AllowAny, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, MagicLink, ResetPasswordLink
from users.serializers import (
  RetrieveUserExistsSerializer, RetrieveCurrentUserSerializer,
  UpdateUserPasswordSerializer, RetrieveMagicLinkSerializer,
  LoginSerializer, UpdateUserEmailSerializer,
  ForgotPasswordSerializer, ResetPasswordSerializer
)


class RetrieveUserExistsView(RetrieveAPIView):
  lookup_field = 'email'
  permission_classes = (AllowAny, )
  queryset = User.objects.all()
  serializer_class = RetrieveUserExistsSerializer


class RetrieveCurrentUserView(RetrieveAPIView):
  lookup_field = None
  permission_classes = (IsAuthenticated, )
  serializer_class = RetrieveCurrentUserSerializer

  def get_object(self):
    return self.request.user

class UpdateUserPasswordView(UpdateAPIView):
  allowed_methods = ('OPTIONS', 'PUT', )
  lookup_field = None
  permission_classes = (IsAuthenticated, )
  serializer_class = UpdateUserPasswordSerializer

  def get_object(self):
    return self.request.user


class UpdateUserEmailView(UpdateAPIView):
  allowed_methods = ('OPTIONS', 'PUT', )
  lookup_field = None
  permission_classes = (IsAuthenticated, )
  serializer_class = UpdateUserEmailSerializer

  def get_object(self):
    return self.request.user


class RetrieveMagicLinkView(RetrieveAPIView):
  permission_classes = (AllowAny, )
  serializer_class = RetrieveMagicLinkSerializer
  queryset = MagicLink.objects.active()

  def retrieve(self, *args, **kwargs):
    instance = self.get_object()
    user = instance.user
    token, _ = Token.objects.get_or_create(user=user)
    response_data = self.serializer_class(instance, context={'token': token.key}).data
    if not instance.valid_forever:
      instance.delete()
    return Response(response_data)


class CheckTokenView(APIView):
  allowed_methods = ('OPTIONS', 'GET', )
  permission_classes = (AllowAny, )

  def get(self, request, *args, **kwargs):
    return Response({ 'status': 'ok' })

  
class LoginView(APIView):
  allowed_methods = ('OPTIONS', 'POST')
  serializer_class = LoginSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data.get('user')
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
      'id': str(user.id),
      'token': token.key
    })


class ForgotPasswordView(CreateAPIView):
  permission_classes = (AllowAny, )
  serializer_class = ForgotPasswordSerializer


class ResetPasswordView(RetrieveUpdateAPIView):
  allowed_methods = ('OPTIONS', 'GET', 'PUT')
  serializer_class = ResetPasswordSerializer
  queryset = ResetPasswordLink.objects.all()
