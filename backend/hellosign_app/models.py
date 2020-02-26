# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

from base.models import BaseModel


class HelloSignSavedCallback(BaseModel):
  post = JSONField(
    verbose_name=_('post'),
    default=dict,
  )
  data = JSONField(
    verbose_name=_('data'),
    default=dict,
  )
  body = models.TextField(
    verbose_name=_('body'),
    default='',
  )
  traceback = models.TextField(
    verbose_name=_('traceback'),
    default='',
    null=True
  )
  caller = models.TextField(
    verbose_name=_('caller'),
    default='hellosign_app'
  )

  def __str__(self):
    return 'hellosign_app calback: {}'.format(self.id)

  class Meta:
    verbose_name = _('hellosign_app callback')
    verbose_name_plural = _('hellosign_app callbacks')


def signed_document_path(instance, filename):
  return 'hellosign/{0}/{1}/{2}'.format(
    instance.__class__.__name__, instance.id, filename)


class HelloSignSignatureRequest(BaseModel):
  signature_request_id = models.CharField(
    verbose_name=_('signature request id'),
    max_length=255,
    blank=True,
  )

  user_signature_id = models.CharField(
    verbose_name=_('user_signature_id signature id'),
    max_length=255,
    blank=True,
  )

  user_signed = models.BooleanField(
    verbose_name=_('user signed'),
    default=False,
  )

  signed_document = models.FileField(
    verbose_name=_('document'),
    upload_to=signed_document_path,
    max_length=1000,
    blank=True,
    null=True,
  )

  def __str__(self):
    return 'HSSignature request {}'.format(self.signature_request_id)

  class Meta:
    verbose_name = _('HelloSign signature request')
    verbose_name_plural = _('HelloSign signature requests')
    ordering = ('-created', )
