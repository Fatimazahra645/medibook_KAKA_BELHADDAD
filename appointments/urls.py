from django.urls import path
from .views import (book_appointment_view,cancel_appointment_view,reschedule_appointment_view,
    get_slots_view,appointment_success_view,create_consultation_view,
    confirm_appointment_view,doctor_cancel_appointment_view,mark_absent_view)
urlpatterns = [
    path("book/<int:doctor_id>/", book_appointment_view, name="book_appointment"),
    path("cancel/<int:appointment_id>/", cancel_appointment_view, name="cancel_appointment"),
    path("reschedule/<int:appointment_id>/", reschedule_appointment_view, name="reschedule_appointment"),
    path("slots/<int:doctor_id>/", get_slots_view, name="get_slots"),
    path("success/", appointment_success_view, name="appointment_success"),
    path("consultation/create/<int:appointment_id>/", create_consultation_view, name="create_consultation"),
    path("confirm/<int:appointment_id>/", confirm_appointment_view, name="confirm_appointment"),
    path("doctor-cancel/<int:appointment_id>/", doctor_cancel_appointment_view, name="doctor_cancel_appointment"),
    path("absent/<int:appointment_id>/", mark_absent_view, name="mark_absent"),
]
