from django.urls import path
from .views import add_review, doctor_detail, edit_doctor_profile, manage_availability, delete_availability
urlpatterns = [
    path("review/<int:doctor_id>/", add_review, name="add_review"),
    path("<int:doctor_id>/", doctor_detail, name="doctor_detail"),
    path("profile/edit/", edit_doctor_profile, name="doctor_profile_edit"),
    path("availability/", manage_availability, name="manage_availability"),
    path("availability/delete/<int:availability_id>/", delete_availability, name="delete_availability"),
]
