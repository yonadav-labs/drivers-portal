from datetime import timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.functional import cached_property

from base.models import BaseModel

from users.managers import UserManager, MagicLinkQueryset


class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(
        verbose_name='Email address',
        unique=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name).strip()

    @property
    def quote_process(self):
      return getattr(self, 'quoteprocess', None)

    @property
    def has_policy(self):
      return hasattr(self, 'policy')

    @cached_property
    def quote_status(self):
      quote = self.quote_process
      return quote.status if quote else None

    def send_welcome_email(self):
        from users.tasks import send_welcome_email_task

        return send_welcome_email_task.delay(self.id)


def magic_link_expire():
    return timezone.now() + timedelta(days=1)


class MagicLink(BaseModel):
    expire_on = models.DateTimeField(
        verbose_name='expire on',
        default=magic_link_expire
    )
    user = models.ForeignKey(
        verbose_name='user',
        to=User,
        on_delete=models.CASCADE
    )
    redirect_to = models.CharField(
        verbose_name='redirect to',
        max_length=255,
        blank=True,
        null=True
    )
    valid_forever = models.BooleanField(
        verbose_name='valid forever',
        default=False
    )

    objects = MagicLinkQueryset.as_manager()

    def is_expired(self):
        return timezone.now() > self.expire_on

    def get_url(self):
      return f"{settings.FRONTEND_URL}/magic_link/{str(self.id)}/"


class ResetPasswordLink(BaseModel):
    expire_on = models.DateTimeField(
        verbose_name='expire on',
        default=magic_link_expire
    )
    user = models.ForeignKey(
        verbose_name='user',
        to=User,
        on_delete=models.CASCADE
    )

    def get_url(self):
        return f"{settings.FRONTEND_URL}/reset-password/{str(self.id)}/"
