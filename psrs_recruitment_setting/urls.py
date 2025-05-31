from rest_framework_nested import routers

from django.urls import path, include
from .views import CompanyViewSet

setting_router = routers.SimpleRouter()

setting_router.register("company", CompanyViewSet)


urlpatterns = [
    path("", include(setting_router.urls)),
]
