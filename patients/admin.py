from django.contrib import admin
from django import forms
from .models import Patient


class PatientAdminForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.models import User
        # Limiter aux utilisateurs avec rôle PATIENT sans profil existant
        existing_patient_user_ids = (
            Patient.objects.exclude(pk=self.instance.pk if self.instance.pk else None)
            .values_list("user_id", flat=True)
        )
        self.fields["user"].queryset = User.objects.filter(
            role=User.Role.PATIENT
        ).exclude(id__in=existing_patient_user_ids)
        self.fields["user"].label = "Utilisateur (rôle Patient)"
        self.fields["phone"].label = "Téléphone"
        self.fields["birth_date"].label = "Date de naissance"


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    form = PatientAdminForm

    list_display = ("get_full_name", "get_email", "phone", "birth_date")
    search_fields = ("user__first_name", "user__last_name", "user__email", "phone")
    ordering = ("user__last_name",)

    fieldsets = (
        ("Compte utilisateur", {
            "fields": ("user",),
        }),
        ("Informations personnelles", {
            "fields": ("phone", "birth_date"),
        }),
    )

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
    get_full_name.short_description = "Patient"

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"
