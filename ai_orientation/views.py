from django.shortcuts import render
from .services import suggest_speciality


def ai_orientation_view(request):
    suggestion = None
    if request.method == "POST":
        reason = request.POST.get("reason", "")
        if reason:
            suggestion = suggest_speciality(reason)

    return render(request, "ai_orientation/orientation.html", {
        "suggestion": suggestion
    })
