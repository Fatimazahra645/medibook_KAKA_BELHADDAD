from django.db import models
from accounts.models import User
from doctors.models import Doctor, Speciality
from patients.models import Patient

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING"
        CONFIRMED = "CONFIRMED"
        CANCELLED = "CANCELLED"
        COMPLETED = "COMPLETED"
        ABSENT = "ABSENT"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)

    date = models.DateField()
    time = models.TimeField()

    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "date", "time"],
                name="unique_doctor_slot"
            )
        ]