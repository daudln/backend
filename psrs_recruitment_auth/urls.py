from django.urls import include, path
from rest_framework.authtoken import views as auth_views
from rest_framework_nested import routers

from .views import UserViewSet

router = routers.DefaultRouter()

router.register("api/users", UserViewSet)

urlpatterns = [
    path("login/", auth_views.obtain_auth_token, name="api_token_auth"),
    path("", include(router.urls)),
]
