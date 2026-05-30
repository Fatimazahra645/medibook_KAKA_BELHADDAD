from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("doctors/", views.doctors_view, name="doctors"),

    path("appointments/", include("appointments.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("ai/", include("ai_orientation.urls")),
]
