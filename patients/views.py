from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Patient
from .forms import PatientProfileForm
@login_required
def edit_profile_view(request):
    if request.user.role!="PATIENT": return HttpResponseForbidden()
    patient=get_object_or_404(Patient,user=request.user)
    if request.method=="POST":
        form=PatientProfileForm(request.POST)
        if form.is_valid():
            d=form.cleaned_data
            request.user.first_name=d.get("first_name",""); request.user.last_name=d.get("last_name","")
            request.user.email=d.get("email",""); request.user.save()
            patient.phone=d.get("phone",""); patient.birth_date=d.get("birth_date"); patient.save()
            messages.success(request,"Profil mis a jour."); return redirect("patient_dashboard")
    else:
        form=PatientProfileForm(initial={"first_name":request.user.first_name,"last_name":request.user.last_name,
            "email":request.user.email,"phone":patient.phone,"birth_date":patient.birth_date})
    return render(request,"patients/profile_edit.html",{"form":form})
