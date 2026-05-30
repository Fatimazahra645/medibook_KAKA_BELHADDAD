from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .utils import get_dashboard_url
from doctors.models import Doctor

User = get_user_model()


def home(request):
    return render(request, "core/home.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect(get_dashboard_url(request.user))

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(get_dashboard_url(user))

        return render(request, "accounts/login.html", {
            "error": "Nom d'utilisateur ou mot de passe incorrect."
        })

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {
                "error": "Ce nom d'utilisateur est déjà utilisé."
            })

        # Crée l'utilisateur avec rôle PATIENT
        # Le signal accounts/signals.py crée automatiquement le profil Patient
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role="PATIENT"
        )

        return redirect("login")

    return render(request, "accounts/register.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def doctors_view(request):
    doctors = Doctor.objects.filter(is_active=True).select_related("user", "speciality")
    return render(request, "doctors/list.html", {"doctors": doctors})
