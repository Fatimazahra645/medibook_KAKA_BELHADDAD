import json
from datetime import date as date_type

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages

from doctors.models import Doctor
from patients.models import Patient
from .models import Appointment
from .services import book_appointment, get_available_slots


@login_required
def book_appointment_view(request, doctor_id):
    if request.user.role != "PATIENT":
        return HttpResponseForbidden("Seuls les patients peuvent réserver un rendez-vous.")

    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return render(request, "appointments/book.html", {
            "error": "Profil patient introuvable. Veuillez contacter l'administration."
        })

    doctor = get_object_or_404(Doctor, pk=doctor_id, is_active=True)

    error = None
    selected_date = None

    if request.method == "POST":
        selected_date_str = request.POST.get("date", "")
        selected_time_str = request.POST.get("time", "")
        reason = request.POST.get("reason", "").strip()

        if not selected_date_str or not selected_time_str or not reason:
            error = "Veuillez remplir tous les champs."
        else:
            try:
                from datetime import datetime
                selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
                selected_time = datetime.strptime(selected_time_str, "%H:%M").time()

                if selected_date < date_type.today():
                    error = "Vous ne pouvez pas réserver une date dans le passé."
                else:
                    appointment, message = book_appointment(
                        patient=patient,
                        doctor=doctor,
                        speciality=doctor.speciality,
                        date=selected_date,
                        time=selected_time,
                        reason=reason,
                    )
                    if appointment:
                        return redirect("appointment_success")
                    else:
                        error = message

            except ValueError:
                error = "Date ou heure invalide."

        if selected_date_str:
            try:
                from datetime import datetime
                selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
            except ValueError:
                selected_date = None

    today_str = date_type.today().isoformat()

    return render(request, "appointments/book.html", {
        "doctor": doctor,
        "error": error,
        "selected_date": selected_date.isoformat() if selected_date else "",
        "today": today_str,
    })


@login_required
def cancel_appointment_view(request, appointment_id):
    """Le patient annule son rendez-vous. Notification créée pour le médecin."""
    if request.user.role != "PATIENT":
        return HttpResponseForbidden()

    patient = get_object_or_404(Patient, user=request.user)
    appointment = get_object_or_404(
        Appointment, pk=appointment_id, patient=patient
    )

    if appointment.status not in ["PENDING", "CONFIRMED"]:
        messages.error(request, "Ce rendez-vous ne peut plus être annulé.")
        return redirect("patient_dashboard")

    if request.method == "POST":
        appointment.status = "CANCELLED"
        appointment.save()

        # Notification au médecin
        from notifications.services import notify_doctor_cancellation
        notify_doctor_cancellation(appointment)

        messages.success(request, "Votre rendez-vous a été annulé.")
        return redirect("patient_dashboard")

    return render(request, "appointments/cancel_confirm.html", {
        "appointment": appointment
    })


@login_required
def reschedule_appointment_view(request, appointment_id):
    """Le patient modifie la date/heure de son rendez-vous."""
    if request.user.role != "PATIENT":
        return HttpResponseForbidden()

    patient = get_object_or_404(Patient, user=request.user)
    appointment = get_object_or_404(
        Appointment, pk=appointment_id, patient=patient
    )

    if appointment.status not in ["PENDING", "CONFIRMED"]:
        messages.error(request, "Ce rendez-vous ne peut plus être modifié.")
        return redirect("patient_dashboard")

    error = None
    selected_date = None

    if request.method == "POST":
        selected_date_str = request.POST.get("date", "")
        selected_time_str = request.POST.get("time", "")

        if not selected_date_str or not selected_time_str:
            error = "Veuillez sélectionner une date et un créneau."
        else:
            try:
                from datetime import datetime
                selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
                selected_time = datetime.strptime(selected_time_str, "%H:%M").time()

                if selected_date < date_type.today():
                    error = "Vous ne pouvez pas choisir une date dans le passé."
                else:
                    # Vérifier que le nouveau créneau est disponible
                    available_slots = get_available_slots(appointment.doctor, selected_date)
                    time_str = selected_time.strftime("%H:%M")

                    if time_str not in available_slots:
                        error = "Ce créneau n'est pas disponible."
                    else:
                        # Vérifier qu'il n'est pas déjà pris (par quelqu'un d'autre)
                        conflict = Appointment.objects.filter(
                            doctor=appointment.doctor,
                            date=selected_date,
                            time=selected_time,
                            status__in=["PENDING", "CONFIRMED"]
                        ).exclude(pk=appointment.pk).exists()

                        if conflict:
                            error = "Ce créneau est déjà réservé."
                        else:
                            appointment.date = selected_date
                            appointment.time = selected_time
                            appointment.status = "PENDING"
                            appointment.save()

                            # Notification au médecin
                            from notifications.services import notify_doctor_reschedule
                            notify_doctor_reschedule(appointment)

                            messages.success(request, "Votre rendez-vous a été modifié.")
                            return redirect("patient_dashboard")

            except ValueError:
                error = "Date ou heure invalide."

        if selected_date_str:
            try:
                from datetime import datetime
                selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
            except ValueError:
                selected_date = None

    today_str = date_type.today().isoformat()

    return render(request, "appointments/reschedule.html", {
        "appointment": appointment,
        "error": error,
        "selected_date": selected_date.isoformat() if selected_date else "",
        "today": today_str,
    })


@login_required
def get_slots_view(request, doctor_id):
    if request.user.role != "PATIENT":
        return JsonResponse({"slots": [], "error": "Accès refusé."}, status=403)

    doctor = get_object_or_404(Doctor, pk=doctor_id, is_active=True)
    date_str = request.GET.get("date", "")
    exclude_appointment_id = request.GET.get("exclude", None)

    if not date_str:
        return JsonResponse({"slots": [], "error": "Paramètre date manquant."})

    try:
        from datetime import datetime
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if target_date < date_type.today():
            return JsonResponse({"slots": [], "error": "Date dans le passé."})
    except ValueError:
        return JsonResponse({"slots": [], "error": "Format de date invalide."})

    slots = get_available_slots(
        doctor, target_date,
        exclude_appointment_id=int(exclude_appointment_id) if exclude_appointment_id else None
    )
    return JsonResponse({"slots": slots})


@login_required
def appointment_success_view(request):
    return render(request, "appointments/success.html")