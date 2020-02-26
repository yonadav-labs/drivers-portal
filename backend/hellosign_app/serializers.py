from rest_framework import serializers


class CompleteSignatureSerializer(serializers.Serializer):
  signature_id = serializers.CharField(
    required=True, allow_blank=False, allow_null=False)
