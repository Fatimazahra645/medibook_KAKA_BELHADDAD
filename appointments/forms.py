from django import forms
from .models import Appointment, Consultation


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["doctor", "speciality", "date", "time", "reason"]


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ["diagnosis", "prescription", "notes"]
        widgets = {
            "diagnosis": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "prescription": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }
