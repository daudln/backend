from django.db import models

from psrs_recruitment_mixin.models import BaseModel


class Company(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    website = models.URLField()
    address = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["email"]),
            models.Index(fields=["phone_number"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["email"], name="unique_email"),
            models.UniqueConstraint(
                fields=["phone_number"], name="unique_phone_number"
            ),
        ]
