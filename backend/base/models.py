import uuid
from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ('-created', )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created = models.DateTimeField(
        verbose_name="Created date",
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        verbose_name="Modified date",
        auto_now=True,
    )