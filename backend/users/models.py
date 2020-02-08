from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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

    objects = MagicLinkQueryset.as_manager()

    def is_expired(self):
        return timezone.now() > self.expire_on
