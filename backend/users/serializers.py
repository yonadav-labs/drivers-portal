from rest_framework import serializers

from users.models import User

class RetrieveUserExistsSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = (
      'email',
    )
    read_only_fields = (
      'email',
    )