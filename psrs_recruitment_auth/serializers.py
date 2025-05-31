from rest_framework import serializers

from psrs_recruitment_auth.models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["phone_number", "address", "date_of_birth", "points"]
        read_only_fields = ["points"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "profile",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        user = User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        # Create the profile instance
        Profile.objects.create(user=user, **profile_data)
        return user
