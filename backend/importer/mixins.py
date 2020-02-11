from django.db import models

from importer.utils import create_hash


class HashedRawMixin(models.Model):
    class Meta:
        abstract = True

    raw_hash = models.CharField(db_index=True, max_length=32, editable=False,)

    def create_hash(self, data):
        return create_hash(data)

    def save(self, *args, **kwargs):
        raw_hash = self.create_hash(self.raw or '')
        if self.raw_hash != raw_hash:
            self.raw_hash = raw_hash
        super().save(*args, **kwargs)
