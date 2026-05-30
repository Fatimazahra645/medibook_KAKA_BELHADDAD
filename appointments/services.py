from datetime import datetime, timedelta, date as date_type
from .models import Appointment
from doctors.models import Availability

WEEKDAY_MAP = {
    0: "MONDAY",
    1: "TUESDAY",
    2: "WEDNESDAY",
    3: "THURSDAY",
    4: "FRIDAY",
    5: "SATURDAY",
    6: "SUNDAY",
}


def get_available_slots(doctor, target_date: date_type, exclude_appointment_id=None) -> list[str]:
    """
    Retourne les créneaux disponibles (HH:MM) pour un médecin à une date.
    exclude_appointment_id : exclure un RDV existant (pour la modification).
    """
    day_name = WEEKDAY_MAP[target_date.weekday()]

    availabilities = Availability.objects.filter(
        doctor=doctor,
        day_of_week=day_name
    )

    if not availabilities.exists():
        return []

    booked_qs = Appointment.objects.filter(
        doctor=doctor,
        date=target_date,
        status__in=["PENDING", "CONFIRMED"]
    )
    if exclude_appointment_id:
        booked_qs = booked_qs.exclude(pk=exclude_appointment_id)

    booked_times = set(booked_qs.values_list("time", flat=True))

    slots = []
    slot_duration = timedelta(minutes=30)

    for availability in availabilities:
        current = datetime.combine(target_date, availability.start_time)
        end = datetime.combine(target_date, availability.end_time)

        while current + slot_duration <= end:
            slot_time = current.time()
            if slot_time not in booked_times:
                slots.append(slot_time.strftime("%H:%M"))
            current += slot_duration

    return sorted(slots)


def book_appointment(patient, doctor, date, time, speciality, reason):
    """Retourne (appointment, message)."""
    available_slots = get_available_slots(doctor, date)
    time_str = time.strftime("%H:%M") if hasattr(time, "strftime") else str(time)[:5]

    if time_str not in available_slots:
        return None, "Ce créneau n'est pas dans les disponibilités du médecin."

    exists = Appointment.objects.filter(
        doctor=doctor, date=date, time=time
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