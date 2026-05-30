from django.contrib.auth import get_user_model

User = get_user_model()


def notify_doctor_cancellation(appointment):
    """
    Crée une notification dans la base pour informer le médecin
    qu'un patient a annulé son rendez-vous.
    """
    try:
        from notifications.models import Notification
        Notification.objects.create(
            user=appointment.doctor.user,
            message=(
                f"Le patient {appointment.patient.user.first_name} "
                f"{appointment.patient.user.last_name} a annulé son rendez-vous "
                f"du {appointment.date.strftime('%d/%m/%Y')} à "
                f"{appointment.time.strftime('%H:%M')}."
            ),
            is_read=False,
        )
    except Exception:
        pass  # Ne pas bloquer l'annulation si la notification échoue


def notify_doctor_reschedule(appointment):
    """
    Crée une notification pour informer le médecin
    qu'un patient a modifié son rendez-vous.
    """
    try:
        from notifications.models import Notification
        Notification.objects.create(
            user=appointment.doctor.user,
            message=(
                f"Le patient {appointment.patient.user.first_name} "
                f"{appointment.patient.user.last_name} a modifié son rendez-vous. "
                f"Nouveau créneau : {appointment.date.strftime('%d/%m/%Y')} à "
                f"{appointment.time.strftime('%H:%M')}."
            ),
            is_read=False,
        )
    except Exception:
        pass