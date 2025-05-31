from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from psrs_recruitment_setting.models import Company
from psrs_recruitment_setting.serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing company instances.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    filterset_fields = ["name", "address", "phone_number", "email", "website"]
    search_fields = ["name", "address", "phone_number", "email", "website"]
    ordering_fields = ["name", "address", "phone_number", "email", "website"]
    ordering = ["name"]

    def destroy(self, request, *args, **kwargs):
        """
        Override the destroy method to add custom behavior.
        """
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
