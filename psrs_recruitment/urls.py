from rest_framework_nested import routers

from django.urls import path, include
from .views import ApplicationViewSet, JobViewSet

recruitment_router = routers.SimpleRouter()

recruitment_router.register("jobs", JobViewSet, basename="jobs")
recruitment_router.register("applications", ApplicationViewSet, basename="applications")


urlpatterns = [
    path("", include(recruitment_router.urls)),
]
