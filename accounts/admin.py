from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    # Colonnes liste
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
        "is_active"
    )

    list_filter = ("role", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    # Formulaire ADD
    add_fieldsets = (
        ("Compte", {
            "fields": ("username", "password1", "password2"),
        }),
        ("Infos personnelles", {
            "fields": ("first_name", "last_name", "email"),
        }),
        ("Rôle", {
            "fields": ("role",),
        }),
    )

    # Formulaire CHANGE
    fieldsets = (
        ("Compte", {
            "fields": ("username", "password"),
        }),
        ("Infos personnelles", {
            "fields": ("first_name", "last_name", "email"),
        }),
        ("Rôle", {
            "fields": ("role", "is_active"),
        }),
    )