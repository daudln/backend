from rest_framework.authtoken.admin import TokenAdmin
from django.contrib import admin
from .models import User, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ["first_name", "last_name", "email", "username"]
    list_display = ["username", "first_name", "last_name", "email", "user_type"]
    list_filter = ["first_name", "last_name"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "user_type",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "user_type",
                )
            },
        ),
    )
    ordering = ["email"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ["user__first_name", "user__last_name", "user__email"]
    list_display = ["user", "phone_number", "address", "date_of_birth", "points"]
    list_filter = ["user__first_name", "user__last_name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user")

    def user(self, obj):
        return obj.user.username if obj.user else None

    user.admin_order_field = "user__username"
    user.short_description = "User"
    user.empty_value_display = "N/A"
    user.admin_order_field = "user__username"
    user.short_description = "User"
    user.empty_value_display = "N/A"
    user.admin_order_field = "user__username"


TokenAdmin.raw_id_fields = ["user"]
