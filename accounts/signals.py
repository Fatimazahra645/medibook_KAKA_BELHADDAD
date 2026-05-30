from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def create_profile_on_user_save(sender, instance, created, **kwargs):
    """
    Quand un utilisateur est créé :
    - Si role=PATIENT  → créer automatiquement un profil Patient
    - Si role=DOCTOR   → créer automatiquement un profil Doctor
    """
    if not created:
        return

    if instance.role == User.Role.PATIENT:
        from patients.models import Patient
        Patient.objects.get_or_create(user=instance)

    elif instance.role == User.Role.DOCTOR:
        from doctors.models import Doctor
        Doctor.objects.get_or_create(
            user=instance,
            defaults={
                "phone": "",
                "address": "",
                "bio": "",
                "experience_years": 0,
                "is_active": True,
            }
        )
