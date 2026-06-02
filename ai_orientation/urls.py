from django.urls import path
from .views import ai_orientation_view

urlpatterns = [
    path("", ai_orientation_view, name="ai_orientation"),
]