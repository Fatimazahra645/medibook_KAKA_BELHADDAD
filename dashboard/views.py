from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden

from patients.models import Patient
from appointments.models import Appointment
from doctors.models import Doctor

from datetime import timedelta
from django.utils import timezone

from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_dashboard(request):
    context = {
        "total_patients": Patient.objects.count(),
        "total_doctors": Doctor.objects.count(),
        "total_appointments": Appointment.objects.count(),
        "pending_count": Appointment.objects.filter(status="PENDING").count(),
        "confirmed_count": Appointment.objects.filter(status="CONFIRMED").count(),
        "cancelled_count": Appointment.objects.filter(status="CANCELLED").count(),
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
def doctor_dashboard(request):
    if request.user.role != "DOCTOR":
        return HttpResponseForbidden("Accès réservé aux médecins.")

    doctor = get_object_or_404(Doctor, user=request.user)

    today = timezone.now().date()
    week_end = today + timedelta(days=7)

    today_appointments = Appointment.objects.filter(doctor=doctor, date=today)
    week_appointments = Appointment.objects.filter(doctor=doctor, date__range=[today, week_end])
    total_appointments = Appointment.objects.filter(doctor=doctor).count()
    cancelled_count = Appointment.objects.filter(doctor=doctor, status="CANCELLED").count()
    confirmed_count = Appointment.objects.filter(doctor=doctor, status="CONFIRMED").count()

    # Notifications non lues
    try:
        from notifications.models import Notification
        unread_notifications = Notification.objects.filter(
            user=request.user, is_read=False
        )
        # Les marquer comme lues après affichage
        unread_notifications.update(is_read=True)
    except Exception:
        unread_notifications = []

    return render(request, "dashboard/doctor_dashboard.html", {
        "doctor": doctor,
        "today_appointments": today_appointments,
        "week_appointments": week_appointments,
        "total_appointments": total_appointments,
        "cancelled_count": cancelled_count,
        "confirmed_count": confirmed_count,
        "unread_notifications": unread_notifications,
    })


@login_required
def patient_dashboard(request):
    if request.user.role != "PATIENT":
        return HttpResponseForbidden("Accès réservé aux patients.")

    patient = get_object_or_404(Patient, user=request.user)

    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        status__in=["PENDING", "CONFIRMED"]
    ).order_by("date", "time")

    past_appointments = Appointment.objects.filter(
        patient=patient,
        status="COMPLETED"
    ).order_by("-date")

    cancelled_appointments = Appointment.objects.filter(
        patient=patient,
        status="CANCELLED"
    ).order_by("-date")

    return render(request, "dashboard/patient_dashboard.html", {
        "patient": patient,
        "upcoming_appointments": upcoming_appointments,
        "past_appointments": past_appointments,
        "cancelled_appointments": cancelled_appointments,
    })


@staff_member_required
def admin_dashboard(request):

    context = {
        "patients_count": Patient.objects.count(),
        "doctors_count": Doctor.objects.count(),
        "appointments_count": Appointment.objects.count(),
        "appointments_today": Appointment.objects.filter(date__date="2026-06-02").count(),
    }

    return render(request, "admin/dashboard.html", context)