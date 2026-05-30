from django.urls import path
from .views import (
    book_appointment_view,
    cancel_appointment_view,
    reschedule_appointment_view,
    get_slots_view,
    appointment_success_view,
)

urlpatterns = [
    path("book/<int:doctor_id>/", book_appointment_view, name="book_appointment"),
    path("cancel/<int:appointment_id>/", cancel_appointment_view, name="cancel_appointment"),
    path("reschedule/<int:appointment_id>/", reschedule_appointment_view, name="reschedule_appointment"),
    path("slots/<int:doctor_id>/", get_slots_view, name="get_slots"),
    path("success/", appointment_success_view, name="appointment_success"),
]