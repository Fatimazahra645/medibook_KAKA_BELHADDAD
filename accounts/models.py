from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.PATIENT)

    def is_patient(self):
        return self.role == self.Role.PATIENT

    def is_doctor(self):
        return self.role == self.Role.DOCTOR