from django.utils import timezone
from rest_framework import serializers

from psrs_recruitment.models import Job, Application


class JobSerializer(serializers.ModelSerializer):
    posted_on = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Job
        fields = [
            "pk",
            "title",
            "description",
            "company",
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
    class Meta:
        model = Application
        fields = [
            "pk",
            "job",
            "created_at",
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
