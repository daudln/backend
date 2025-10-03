from rest_framework import serializers

from psrs_recruitment_auth.models import User, Profile
from djoser import serializers as djoser_serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["phone_number", "address", "date_of_birth", "points"]
        read_only_fields = ["points"]


class UserSerializer(djoser_serializers.UserSerializer):
    profile = ProfileSerializer()

    class Meta(djoser_serializers.UserSerializer.Meta):
        fields = djoser_serializers.UserSerializer.Meta.fields + (
            "first_name",
            "last_name",
            "user_type",
            "profile",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta(djoser_serializers.UserCreateSerializer.Meta):
        fields = djoser_serializers.UserCreateSerializer.Meta.fields + (
            "first_name",
            "last_name",
            "user_type",
        )

        read_only_fields = ["user_type"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def create(self, validated_data):
        return super().create(validated_data)
