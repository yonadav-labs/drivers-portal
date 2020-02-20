from django.conf import settings

from hellosign_sdk import HSClient

from hellosign_app.models import HelloSignSignatureRequest


def get_hsclient():
  return HSClient(api_key=getattr(settings, 'HELLOSIGN_APIKEY'))


def create_t_and_c_signature_request(email, name, policy_number):
  client = get_hsclient()
  template = getattr(settings, 'HELLOSIGN_TERMS_TEMPLATE_ID')
  response = client.send_signature_request_embedded_with_template(
    test_mode=getattr(settings, 'HELLOSIGN_TESTMODE', True),
    client_id=getattr(settings, 'HELLOSIGN_CLIENTID'),
    template_id=template,
    signers=[{
      'role_name': 'Client',
      'email_address': email,
      'name': name,
    }],
    custom_fields=[{
      'name': name,
      'policy_number': policy_number
    }]
  )

  signature_request = HelloSignSignatureRequest.objects.create(
    signature_request_id=response.signature_request_id,
    user_signature_id=response.signatures[0].signature_id,
  )

  return signature_request


def complete_signature(signature_id):
  hsr = HelloSignSignatureRequest.objects.get(
    user_signature_id=signature_id)
  hsr.user_signed=True
  hsr.save()

  hsr.quoteprocessdocuments.is_broker_of_record_signed = True
  hsr.quoteprocessdocuments.save()

  return hsr


def get_signature_url(signature_request_id):
  client = get_hsclient()
  response = client.get_embedded_object(signature_request_id)

  return response.sign_url
