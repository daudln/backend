from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "pk",
            "name",
            "address",
            "phone_number",
            "email",
            "website",
        ]
        read_only_fields = ["pk"]
