import uuid
from django.db import models


class BaseModel(models.Model):
    unique_id = models.UUIDField(editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "psrs_recruitment_auth.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        "psrs_recruitment_auth.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_updated",
    )
    deleted_by = models.ForeignKey(
        "psrs_recruitment_auth.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_deleted",
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
