from .models import Appointment
from doctors.models import Availability


def is_available(doctor, day):
    return Availability.objects.filter(doctor=doctor, day_of_week=day).exists()


def book_appointment(patient, doctor, date, time, speciality, reason):
    """
    Returns a tuple (appointment, message).
    On success: (appointment_object, "Rendez-vous réservé avec succès")
    On conflict: (None, "Ce créneau est déjà réservé")
    """
    exists = Appointment.objects.filter(
        doctor=doctor,
        date=date,
        time=time
    ).exists()

    if exists:
        return None, "Ce créneau est déjà réservé. Veuillez choisir un autre horaire."

    appointment = Appointment.objects.create(
        patient=patient,
        doctor=doctor,
        speciality=speciality,
        date=date,
        time=time,
        reason=reason,
        status="PENDING"
    )

    return appointment, "Rendez-vous réservé avec succès"
