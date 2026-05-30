from django.db import models
from accounts.models import User

class Speciality(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)

    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Availability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    day_of_week = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()