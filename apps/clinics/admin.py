from django.contrib import admin

from .models import Clinic


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "phone",
        "email",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }