from django.db import models
from psrs_recruitment_mixin.models import BaseModel
from psrs_recruitment_setting.models import Company
from psrs_recruitment_auth.models import Profile

class JobLocationChoice(models.TextChoices):
    REMOTE = "REMOTE", "Remote"
    DAR_ES_SALAAM = "DAR_ES_SALAAM", "Dar es Salaam"
    OTHER = "OTHER", "Other"


class Job(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(
        max_length=255,
        choices=JobLocationChoice.choices,
        default=JobLocationChoice.OTHER,
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    qualifications = models.TextField()
    responsibilities = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    deadline = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.company.name}"


class Application(BaseModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cv = models.FileField(upload_to="cvs/", validators=[])
    cover_letter = models.FileField(upload_to="cover_letters/", validators=[])

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.applicant} - {self.job.title}"
