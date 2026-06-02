from django.urls import path
from .views import (
    patient_dashboard,
    doctor_dashboard,
    admin_dashboard
)

urlpatterns = [
    path("patient/", patient_dashboard, name="patient_dashboard"),
    path("doctor/", doctor_dashboard, name="doctor_dashboard"),

    # ❌ NE PAS UTILISER "admin/"
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),

    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
]