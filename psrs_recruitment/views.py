from rest_framework import viewsets
from rest_framework import permissions
from psrs_recruitment_utils.permissions import IsAdminUserOrReadOnly

from psrs_recruitment.models import Application, Job
from psrs_recruitment.serializers import JobSerializer, ApplicationSerializer


class JobViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Job instances.
    """

    queryset = Job.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = JobSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Application instances.
    """

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(applicant=self.request.user.profile)
