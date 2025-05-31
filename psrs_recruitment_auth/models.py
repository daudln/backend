from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from psrs_recruitment_mixin.models import BaseModel


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    email = models.EmailField(
        unique=True,
        error_messages={
            _("unique"): _("A user with that email already exists."),
        },
        help_text=_("Required. Enter a valid email address."),
        verbose_name=_("Email address"),
    )

    def __str__(self):
        return self.email

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["email"]

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure the email is unique and lowercase.
        """
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)


class Profile(BaseModel):
    """
    Profile model that extends the user model. Including applicant points
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["user__email"]
