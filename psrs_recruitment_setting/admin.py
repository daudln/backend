from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "phone_number",
        "website",
        "address",
        "created_by",
        "updated_by",
        "is_active",
        "is_deleted",
        "deleted_at",
        "deleted_by",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "email", "phone_number")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "email", "phone_number", "website", "address")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {"fields": ("name", "email", "phone_number", "website", "address")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("created_by", "updated_by")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.is_deleted = True
        obj.save()
        self.message_user(request, "Company deleted successfully.")

    def get_fieldsets(self, request, obj=None):
        if obj:
            return self.fieldsets
        return super().get_fieldsets(request, obj)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return self.list_display
        return tuple(
            field
            for field in self.list_display
            if field not in ("created_by", "updated_by")
        )
