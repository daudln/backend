from psrs_recruitment_auth.models import User
from rest_framework import viewsets, permissions
from psrs_recruitment_auth.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
