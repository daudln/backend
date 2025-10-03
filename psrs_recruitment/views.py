from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from psrs_recruitment_utils.permissions import IsAdminUserOrReadOnly
from psrs_recruitment.filters import JobFilter
from psrs_recruitment.models import Application, Job
from psrs_recruitment.serializers import (
    ApplicationSerializer,
    ApplyJobSerializer,
    JobSerializer,
)


class JobViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Job instances.
    """

    queryset = Job.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = JobSerializer
    lookup_field = "unique_id"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobFilter
    search_fields = ["title", "company__name", "location"]
    ordering_fields = ["title", "company", "location", "salary"]

    @action(
        detail=True,
        methods=["post"],
        url_path="apply",
        permission_classes=[permissions.IsAuthenticated],
    )
    def apply(self, request, unique_id=None):
        job = self.get_object()
        context = self.get_serializer_context()
        context["job"] = job
        context["applicant"] = request.user.profile
        self.get_serializer_context()["applicant"] = request.user.profile
        serializer = ApplyJobSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        if job.deadline < timezone.now():
            raise serializers.ValidationError("The application deadline has passed.")

        if job.applications.filter(applicant=request.user.profile).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Application instances.
    """

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                job__unique_id=self.kwargs["job_unique_id"],
                applicant=self.request.user.profile,
            )
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["job_unique_id"] = self.kwargs["job_unique_id"]
        return context

    @action(
        detail=False,
        methods=["get"],
        url_path="my-applications",
        permission_classes=[permissions.IsAuthenticated],
    )
    def my_applications(self, request):
        self.queryset = self.queryset.filter(applicant=request.user.profile)
        return self.list(request)
