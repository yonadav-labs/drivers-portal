from rest_framework import serializers

from base.tasks import send_user_reset_password_task
from base.emails import send_notification
from users.models import User, MagicLink, ResetPasswordLink


class RetrieveUserExistsSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ('email', )
    read_only_fields = ('email', )



class RetrieveCurrentUserSerializer(serializers.ModelSerializer):
  has_usable_password = serializers.SerializerMethodField()
  quote_status = serializers.SerializerMethodField()
  has_policy = serializers.SerializerMethodField()

  def get_has_usable_password(self, obj):
    return obj.has_usable_password()

  def get_quote_status(self, obj):
    return obj.quote_status

  def get_has_policy(self, obj):
    return obj.has_policy
  
  class Meta:
    model = User
    fields = (
      'id', 'email', 'has_usable_password', 'quote_status', 
      'has_policy', 'quoteprocess'
    )
    read_only_fields = ('id', 'email', )


class UpdateUserPasswordSerializer(serializers.ModelSerializer):
  password = serializers.CharField(min_length=8, write_only=True)
  has_usable_password = serializers.SerializerMethodField()

  def get_has_usable_password(self, obj):
    return obj.has_usable_password()

  def update(self, instance, validated_data):
    instance.set_password(validated_data.get('password'))
    instance.save()

    send_notification(2, instance.quoteprocess)

    return instance

  class Meta:
    model = User
    fields = ('id', 'email', 'password', 'has_usable_password')
    read_only_fields = ('id', 'email', )
  

class UpdateUserEmailSerializer(serializers.ModelSerializer):

  def update(self, instance, validated_data):
    email = validated_data.get('email')
    if User.objects.filter(email=email).exists():
      raise serializers.ValidationError('This email is already registered as user')
    instance.quote_process.email = email
    instance.quote_process.save()
    instance.email = email
    instance.save()
    return instance

  class Meta:
    model = User
    fields = ('id', 'email')


class RetrieveMagicLinkSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(source='user.email', read_only=True)
  token = serializers.SerializerMethodField()

  def get_token(self, obj):
    return self.context.get('token')

  class Meta:
    model = MagicLink
    fields = ('id', 'email', 'token')
    read_only_fields = ('id', 'email')


class LoginSerializer(serializers.Serializer):
  user = serializers.EmailField(write_only=True)
  password = serializers.CharField(write_only=True)

  def validate_user(self, value):
    try: 
      user = User.objects.get(email=value)
    except User.DoesNotExist:
      raise serializers.ValidationError(
          'Incorrect email or password'
      )
    return user
  
  def validate(self, data):
    user = data.get('user')
    password = data.get('password')
    if not user.check_password(password):
      raise serializers.ValidationError({
        "user": [
          'Incorrect email or password'
        ]
      })
    return data

  
class ForgotPasswordSerializer(serializers.Serializer):
  email = serializers.EmailField(write_only=True)

  def create(self, validated_data):
    email = validated_data.get('email')
    try:
      user = User.objects.get(email=email)
      link = ResetPasswordLink.objects.create(user=user)
      send_user_reset_password_task.delay(str(link.id))
    except User.DoesNotExist:
      pass
    return {}


class ResetPasswordSerializer(serializers.ModelSerializer):
  password = serializers.CharField(min_length=8, write_only=True)

  def update(self, instance, validated_data):
    instance.user.set_password(validated_data.get('password'))
    instance.user.save()
    return instance
  
  class Meta:
    model = ResetPasswordLink
    fields = ('id', 'password')
