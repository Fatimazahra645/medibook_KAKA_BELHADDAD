from django.db import models
from accounts.models import User


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        APPOINTMENT = "APPOINTMENT", "Appointment"
        REMINDER = "REMINDER", "Reminder"
        SYSTEM = "SYSTEM", "System"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM
    )

    appointment = models.ForeignKey(
        "appointments.Appointment",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"

    def mark_as_read(self):
        self.is_read = True
        self.save()