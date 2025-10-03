from django.urls import include, path
from rest_framework_nested import routers

from .views import ApplicationViewSet, JobViewSet

router = routers.DefaultRouter()

router.register("jobs", JobViewSet)

job_router = routers.NestedDefaultRouter(router, "jobs", lookup="job")
job_router.register("applications", ApplicationViewSet, basename="applications")
router.register("applications", ApplicationViewSet, basename="applications")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(job_router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
