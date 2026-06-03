from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("doctors/", views.doctors_view, name="doctor_list"),
    path("doctors/", include("doctors.urls")),
    path("appointments/", include("appointments.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("ai/", include("ai_orientation.urls")),
    path("patients/", include("patients.urls")),
    path("notifications/", include("notifications.urls")),
    # path("password-reset/", include("django.contrib.auth.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
