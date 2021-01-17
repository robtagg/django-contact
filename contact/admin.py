from django.contrib import admin

from . import models


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["label", "email_recipients"]


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email_address", "department", "created_at"]
    list_filter = ["created_at"]
    fieldsets = (
        ("Details", {"fields": ["name", "email_address", "department", "message"]}),
        ("Metadata", {"fields": ["ip_address", "created_at"]}),
    )
