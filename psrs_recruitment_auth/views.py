from psrs_recruitment_auth.models import User
from rest_framework import permissions, mixins, viewsets
from psrs_recruitment_auth.serializers import (
    LoginSerializer,
    UserRegistrationSerializer,
    UserCreateSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=False,
        methods=["post"],
        url_path="register",
        permission_classes=[permissions.AllowAny],
    )
    def register(self, request):
        """
        Register a new user.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User created successfully", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """
        Retrieve the authenticated user's profile.
        """
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request):
        """
        Logout the authenticated user.
        """
        request.user.auth_token.delete()
        return Response(
            {"message": "Logout successful"}, status=status.HTTP_204_NO_CONTENT
        )


class LoginView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    queryset = ...
