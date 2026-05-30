from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("user", "speciality", "is_active")
    search_fields = ("user__username", "phone")
    list_filter = ("speciality", "is_active")