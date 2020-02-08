from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

class ApiStatusView(APIView):
  allowed_methods = ('GET', )
  permission_classes = (AllowAny, )

  def get(self, request, *args, **kwargs):
    return Response({ 'status': 'ok' })