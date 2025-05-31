from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "company", "created_at", "updated_at")
    search_fields = ("title", "company__name")
    list_filter = ("company",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "job",
        "applicant",
        "cv",
        "cover_letter",
        "created_at",
        "updated_at",
    )
    search_fields = ("job__title", "applicant__username", "applicant__email")
    list_filter = ("job", "applicant")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
