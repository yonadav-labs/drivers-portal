import hashlib
import hmac
import json

from django.conf import settings
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView

from hellosign_app.models import HelloSignSavedCallback
from hellosign_app.tasks import save_signed_document, single_signature


class HelloSignCallbackView(APIView):

  def post(self, request, *args, **kwargs):
    data = json.loads(request.data.get('json', "{}"))
    event = data.get('event', {})
    apikey = settings.HELLOSIGN_APIKEY

    # Verify hash
    event_time = event.get('event_time')
    event_type = event.get('event_type')
    event_hash = event.get('event_hash')

    if hmac.new(
        apikey.encode(),
        str((event_time + event_type)).encode(),
        hashlib.sha256).hexdigest() != event_hash:
      raise Http404

    if event_type == 'signature_request_all_signed':
      signature_request_id = data.get(
        'signature_request', {}).get('signature_request_id')
      if signature_request_id:
        save_signed_document.delay(signature_request_id)
    elif event_type == 'signature_request_signed':
      signature_id = event.get('event_metadata', {}).get(
        'related_signature_id', None)
      if signature_id:
        single_signature.delay(signature_id)

    HelloSignSavedCallback.objects.create(
      post=request.POST, data=data, body=data
    )

    return Response("Hello API Event Received")
