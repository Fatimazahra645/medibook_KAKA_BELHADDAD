from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),

    path("doctors/", include("doctors.urls")),
    path("appointments/", include("appointments.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("ai/", include("ai_orientation.urls")),
    path("patients/", include("patients.urls")),
    path("notifications/", include("notifications.urls")),
]

# ✅ OPTION 1 (standard Django)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 🔥 OPTION 2 (FORCE FIX Docker / runserver)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

print("VERSION 2 - CLEAN URLS")