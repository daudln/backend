from rest_framework.authtoken import views as auth_views

from django.urls import path, include
from rest_framework_nested import routers

from .views import UserViewSet

auth_router = routers.SimpleRouter()

auth_router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(auth_router.urls)),
    path("login/", auth_views.obtain_auth_token, name="api_token_auth"),
]
