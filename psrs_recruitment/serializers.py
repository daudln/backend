from django.utils import timezone
from rest_framework import serializers

from psrs_recruitment.models import Job, Application
from psrs_recruitment_setting.serializers import CompanySerializer


class JobSerializer(serializers.ModelSerializer):
    posted_on = serializers.DateTimeField(source="created_at", read_only=True)
    company_detail = CompanySerializer(read_only=True, source="company")

    class Meta:
        model = Job
        fields = [
            "pk",
            "unique_id",
            "title",
            "description",
            "company",
            "company_detail",
            "responsibilities",
            "qualifications",
            "salary",
            "location",
            "posted_on",
            "deadline",
        ]
        read_only_fields = ["pk", "created_at"]
        extra_kwargs = {
            "title": {"required": True},
            "description": {"required": True},
            "company": {"required": True},
        }


class ApplicationSerializer(serializers.ModelSerializer):
    job_detail = JobSerializer(read_only=True, source="job")

    class Meta:
        model = Application
        fields = [
            "pk",
            "job",
            "created_at",
            "updated_at",
            "cv",
            "cover_letter",
            "job_detail",
        ]
        read_only_fields = ["pk", "created_at"]
        extra_kwargs = {
            "job": {"required": True},
        }

    def validate_job(self, value):
        if value.deadline < timezone.now():
            raise serializers.ValidationError("The application deadline has passed.")
        return value

    def create(self, validated_data):
        job = validated_data["job"]

        if job.applications.filter(
            applicant=self.context["request"].user.profile
        ).exists():
            raise serializers.ValidationError("You have already applied for this job.")

        applicant_point = 1

        if job.location == "REMOTE":
            applicant_point = 3
        elif job.location == "DSM":
            applicant_point = 2

        profile = self.context["request"].user.profile
        profile.points += applicant_point
        profile.save()
        validated_data["applicant"] = profile
        application = super().create(validated_data)
        return application


class ApplyJobSerializer(serializers.Serializer):
    cv = serializers.FileField()
    cover_letter = serializers.FileField()
    job_detail = JobSerializer(read_only=True, source="job")

    class Meta:
        fields = ["cv", "cover_letter", "job_detail"]
        read_only_fields = ["job_detail"]
        extra_kwargs = {
            "cv": {"required": True},
            "cover_letter": {"required": True},
        }

    def create(self, validated_data):
        job = self.context.get("job")
        user = self.context["request"].user

        if job.applications.filter(applicant=user.profile).exists():
            raise serializers.ValidationError("You have already applied for this job.")

        applicant_point = 1

        if job.location == "REMOTE":
            applicant_point = 3
        elif job.location == "DSM":
            applicant_point = 2

        profile = user.profile
        profile.points += applicant_point
        profile.save()

        application = Application.objects.create(
            job=job,
            applicant=profile,
            cv=validated_data["cv"],
            cover_letter=validated_data["cover_letter"],
        )
        return application
