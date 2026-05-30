from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Formulaire simplifié de création d'un utilisateur."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre les champs importants obligatoires
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True
        self.fields["role"].required = True
        # Libellés en français
        self.fields["username"].label = "Nom d'utilisateur"
        self.fields["first_name"].label = "Prénom"
        self.fields["last_name"].label = "Nom"
        self.fields["email"].label = "Email"
        self.fields["role"].label = "Rôle"
        self.fields["password1"].label = "Mot de passe"
        self.fields["password2"].label = "Confirmation du mot de passe"


class CustomUserChangeForm(UserChangeForm):
    """Formulaire simplifié de modification d'un utilisateur."""

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "role", "is_active")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Colonnes affichées dans la liste
    list_display = ("username", "first_name", "last_name", "email", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)

    # Formulaire d'AJOUT : sections affichées
    add_fieldsets = (
        ("Informations de connexion", {
            "fields": ("username", "password1", "password2"),
        }),
        ("Informations personnelles", {
            "fields": ("first_name", "last_name", "email"),
        }),
        ("Rôle", {
            "fields": ("role",),
        }),
    )

    # Formulaire de MODIFICATION : sections affichées
    fieldsets = (
        ("Informations de connexion", {
            "fields": ("username", "password"),
        }),
        ("Informations personnelles", {
            "fields": ("first_name", "last_name", "email"),
        }),
        ("Rôle et statut", {
            "fields": ("role", "is_active"),
        }),
    )
