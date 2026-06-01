from django.contrib import admin
from django import forms
from .models import Doctor, Speciality, Availability


class AvailabilityInline(admin.TabularInline):
    """Permet de gérer les disponibilités directement depuis la fiche médecin."""
    model = Availability
    extra = 1
    fields = ("day_of_week", "start_time", "end_time")
    verbose_name = "Disponibilité"
    verbose_name_plural = "Disponibilités"


class DoctorAdminForm(forms.ModelForm):
    """Formulaire personnalisé pour l'admin Doctor."""

    class Meta:
        model = Doctor
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.models import User
        # Limiter le champ user aux utilisateurs ayant le rôle DOCTOR
        # et qui n'ont pas encore de profil Doctor (sauf l'instance actuelle)
        existing_doctor_user_ids = (
            Doctor.objects.exclude(pk=self.instance.pk if self.instance.pk else None)
            .values_list("user_id", flat=True)
        )
        self.fields["user"].queryset = User.objects.filter(
            role=User.Role.DOCTOR
        ).exclude(id__in=existing_doctor_user_ids)
        self.fields["user"].label = "Utilisateur (rôle Médecin)"
        self.fields["user"].help_text = (
            "Seuls les utilisateurs avec le rôle 'Médecin' apparaissent ici. "
            "Si la liste est vide, créez d'abord un utilisateur avec le rôle Médecin."
        )
        self.fields["speciality"].label = "Spécialité"
        self.fields["phone"].label = "Téléphone"
        self.fields["address"].label = "Adresse du cabinet"
        self.fields["image"].label = "Photo de profile"
        self.fields["bio"].label = "Description / Biographie"
        self.fields["experience_years"].label = "Années d'expérience"
        self.fields["is_active"].label = "Actif"


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    form = DoctorAdminForm
    inlines = [AvailabilityInline]

    list_display = ("get_full_name", "get_speciality", "phone", "is_active")
    list_filter = ("speciality", "is_active")
    search_fields = ("user__first_name", "user__last_name", "user__email", "phone")
    ordering = ("user__last_name",)

    fieldsets = (
        ("Compte utilisateur", {
            "fields": ("user",),
        }),
        ("Informations professionnelles", {
            "fields": ("speciality", "phone", "address", "experience_years", "image"),
        }),
        ("Description", {
            "fields": ("bio",),
        }),
        ("Statut", {
            "fields": ("is_active",),
        }),
    )

    def get_full_name(self, obj):
        return f"Dr. {obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
    get_full_name.short_description = "Médecin"

    def get_speciality(self, obj):
        return obj.speciality.name if obj.speciality else "—"
    get_speciality.short_description = "Spécialité"


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["name"].label = "Nom de la spécialité"
        form.base_fields["description"].label = "Description"
        return form
