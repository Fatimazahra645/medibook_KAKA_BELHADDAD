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

            # sécurité: vérifier résultat IA
            if results and "speciality" in results[0]:

                top_speciality_name = results[0]["speciality"]

                # SAFE VERSION (évite crash CI/CD)
                speciality_obj = Speciality.objects.filter(
                    name__iexact=top_speciality_name
                ).first()

                if speciality_obj:
                    doctors_by_speciality = Doctor.objects.filter(
                        speciality=speciality_obj,
                        is_active=True
                    ).select_related("user", "speciality")

    return render(request, "ai_orientation/orientation.html", {
        "results": results,
        "symptoms": symptoms,
        "doctors_by_speciality": doctors_by_speciality,
    })