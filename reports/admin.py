from django.contrib import admin

from .models import CommunityIssue


@admin.register(CommunityIssue)
class CommunityIssueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "main_category",
        "sub_category",
        "severity",
        "status",
        "created_at",
    )
    list_filter = ("main_category", "severity", "status")
    search_fields = ("description", "sub_category")
    ordering = ("-created_at",)
    list_per_page = 25
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
