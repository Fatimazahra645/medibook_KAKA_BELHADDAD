from django.urls import path
from .views import book_appointment_view, appointment_success_view

urlpatterns = [
    path("book/", book_appointment_view, name="book_appointment"),
    path("success/", appointment_success_view, name="appointment_success"),
]
