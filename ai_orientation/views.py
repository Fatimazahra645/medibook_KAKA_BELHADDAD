from django.shortcuts import render
from .services import suggest_speciality
from doctors.models import Doctor, Speciality



def ai_orientation_view(request):
    results = []
    symptoms = ""
    doctors_by_speciality = []

    if request.method == "POST":
        symptoms = request.POST.get("symptoms", "").strip()
        if symptoms:
            results = suggest_speciality(symptoms, top_n=3)

            # Pour la première spécialité suggérée, chercher les médecins disponibles
            if results:
                top_speciality_name = results[0]["speciality"]
                try:
                    speciality_obj = Speciality.objects.get(name=top_speciality_name)
                    doctors_by_speciality = Doctor.objects.filter(
                        speciality=speciality_obj,
                        is_active=True
                    ).select_related("user", "speciality")
                except Speciality.DoesNotExist:
                    doctors_by_speciality = []

    return render(request, "ai_orientation/orientation.html", {
        "results": results,
        "symptoms": symptoms,
        "doctors_by_speciality": doctors_by_speciality,
    })
