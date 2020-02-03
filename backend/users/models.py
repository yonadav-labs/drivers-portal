from django.db import models
from django.contrib.auth.models import AbstractUser

from base.models import BaseModel

from users.managers import UserManager


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
