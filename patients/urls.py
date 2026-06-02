from django.urls import path
from .views import edit_profile_view
urlpatterns = [path("profile/edit/", edit_profile_view, name="patient_profile_edit")]
