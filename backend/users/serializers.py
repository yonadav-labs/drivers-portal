from rest_framework import serializers

from users.models import User

class RetrieveUserExistsSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ('email', )
    read_only_fields = ('email', )



class RetrieveCurrentUserSerializer(serializers.ModelSerializer):
  has_usable_password = serializers.SerializerMethodField()

  def get_has_usable_password(self, obj):
    return obj.has_usable_password()
  
  class Meta:
    model = User
    fields = ('id', 'email', 'has_usable_password')
    read_only_fields = ('id', 'email', )


class UpdateUserPasswordSerializer(serializers.ModelSerializer):
  password = serializers.CharField(min_length=8, write_only=True)
  has_usable_password = serializers.SerializerMethodField()

  def get_has_usable_password(self, obj):
    return obj.has_usable_password()
  class Meta:
    model = User
    fields = ('id', 'email', 'password', 'has_usable_password')
    read_only_fields = ('id', 'email', )