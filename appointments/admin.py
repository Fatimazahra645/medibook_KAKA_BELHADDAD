from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("get_patient", "get_doctor", "speciality", "date", "time", "status")
    list_filter = ("status", "speciality", "date")
    search_fields = (
        "patient__user__first_name", "patient__user__last_name",
        "doctor__user__first_name", "doctor__user__last_name",
    )
    ordering = ("-date", "-time")
    date_hierarchy = "date"

    fieldsets = (
        ("Participants", {
            "fields": ("patient", "doctor", "speciality"),
        }),
        ("Rendez-vous", {
            "fields": ("date", "time", "reason"),
        }),
        ("Statut", {
            "fields": ("status",),
        }),
    )

    def get_patient(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}".strip() or obj.patient.user.username
    get_patient.short_description = "Patient"

    def get_doctor(self, obj):
        return f"Dr. {obj.doctor.user.first_name} {obj.doctor.user.last_name}".strip() or obj.doctor.user.username
    get_doctor.short_description = "Medecin"
