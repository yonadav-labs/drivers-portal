from io import BytesIO

from django.core.files import File
from django.shortcuts import get_object_or_404

from celery.decorators import task

from hellosign_app.utils import get_hsclient, complete_signature


@task(name="save_signed_document")
def save_signed_document(signature_request_id):
  """
  Task to save an incoming HelloSign document file
    :param signature_request_id:
  :return:
  """

  from hellosign_app.models import HelloSignSignatureRequest

  hellosign_request = get_object_or_404(
    HelloSignSignatureRequest, signature_request_id=signature_request_id)
  client = get_hsclient()

  f = BytesIO()
  result = client.get_signature_request_file(
    signature_request_id=signature_request_id,
    path_or_file=f, file_type='pdf')

  if result:
    hellosign_request.signed_document = File(
      f, "signed_doc_{0}.pdf".format(str(hellosign_request.id)))
    hellosign_request.save()
    hellosign_request.quoteprocessdocuments.broker_record_file = File(
      f, "signed_doc_{0}.pdf".format(str(hellosign_request.id)))
    hellosign_request.quoteprocessdocuments.save()


@task(name="single_signature")
def single_signature(signature_id):
  """
  Task to mark needed models when one signature has been completed
    :param signature_request_id:
  :return:
  """
  complete_signature(signature_id)
