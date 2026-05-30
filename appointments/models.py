from django.db import models
from accounts.models import User
from doctors.models import Doctor, Speciality

class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING"
        CONFIRMED = "CONFIRMED"
        CANCELLED = "CANCELLED"
        COMPLETED = "COMPLETED"
        ABSENT = "ABSENT"

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")

    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)

    date = models.DateField()
    time = models.TimeField()

    reason = models.TextField()

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)