from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .forms import AppointmentForm
from .services import book_appointment
from patients.models import Patient


@login_required
def book_appointment_view(request):
    # Only patients can book appointments
    if request.user.role != "PATIENT":
        return HttpResponseForbidden("Seuls les patients peuvent réserver un rendez-vous.")

    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return render(request, "appointments/book.html", {
            "error": "Profil patient introuvable. Veuillez contacter l'administration."
        })

    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment, message = book_appointment(
                patient=patient,
                doctor=form.cleaned_data["doctor"],
                speciality=form.cleaned_data["speciality"],
                date=form.cleaned_data["date"],
                time=form.cleaned_data["time"],
                reason=form.cleaned_data["reason"]
            )

            if appointment:
                return redirect("appointment_success")
            else:
                return render(request, "appointments/book.html", {
                    "form": form,
                    "error": message
                })

    else:
        form = AppointmentForm()

    return render(request, "appointments/book.html", {"form": form})


@login_required
def appointment_success_view(request):
    return render(request, "appointments/success.html")
