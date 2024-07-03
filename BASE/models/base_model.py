import uuid
from django.db import models


class BaseModels(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    # need to add foreign key for
    # created_by
    # modified_by
    is_active = models.BooleanField(default=True)
    is_archieved = models.BooleanField(default=False)

    class Meta:
        abstract = True
