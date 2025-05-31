from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("psrs_recruitment.urls")),
    path("", include("psrs_recruitment_setting.urls")),
    path("", include("psrs_recruitment_auth.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
