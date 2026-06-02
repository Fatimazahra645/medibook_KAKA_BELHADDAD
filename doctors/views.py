from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from .models import Doctor, Review, Availability
from .forms import ReviewForm, DoctorProfileForm, AvailabilityForm

@login_required
def add_review(request, doctor_id):
    doctor=get_object_or_404(Doctor,id=doctor_id)
    if request.method=="POST":
        form=ReviewForm(request.POST)
        if form.is_valid():
            r=form.save(commit=False); r.doctor=doctor
            try: r.patient=request.user.patient
            except ObjectDoesNotExist: return redirect("login")
            r.save(); messages.success(request,"Avis enregistre.")
            return redirect("doctor_list")
    else: form=ReviewForm()
    return render(request,"doctors/add_review.html",{"form":form,"doctor":doctor})

def doctor_detail(request, doctor_id):
    doctor=get_object_or_404(Doctor,id=doctor_id,is_active=True)
    reviews=Review.objects.filter(doctor=doctor).select_related("patient__user").order_by("-created_at")
    ratings=[r.rating for r in reviews]
    avg=round(sum(ratings)/len(ratings),1) if ratings else None
    return render(request,"doctors/doctor_detail.html",{
        "doctor":doctor,"reviews":reviews,"avg_rating":avg,"review_count":len(ratings)})

@login_required
def edit_doctor_profile(request):
    if request.user.role!="DOCTOR": return HttpResponseForbidden()
    doctor=get_object_or_404(Doctor,user=request.user)
    if request.method=="POST":
        form=DoctorProfileForm(request.POST,request.FILES)
        if form.is_valid():
            d=form.cleaned_data
            request.user.first_name=d.get("first_name",""); request.user.last_name=d.get("last_name","")
            request.user.email=d.get("email",""); request.user.save()
            doctor.phone=d.get("phone",""); doctor.address=d.get("address","")
            doctor.bio=d.get("bio",""); doctor.experience_years=d.get("experience_years") or 0
            if d.get("image"): doctor.image=d["image"]
            doctor.save(); messages.success(request,"Profil mis a jour.")
            return redirect("doctor_dashboard")
    else:
        form=DoctorProfileForm(initial={"first_name":request.user.first_name,"last_name":request.user.last_name,
            "email":request.user.email,"phone":doctor.phone,"address":doctor.address,
            "bio":doctor.bio,"experience_years":doctor.experience_years})
    return render(request,"doctors/profile_edit.html",{"form":form,"doctor":doctor})

@login_required
def manage_availability(request):
    if request.user.role!="DOCTOR": return HttpResponseForbidden()
    doctor=get_object_or_404(Doctor,user=request.user)
    avails=Availability.objects.filter(doctor=doctor).order_by("day_of_week","start_time")
    form=AvailabilityForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        a=form.save(commit=False); a.doctor=doctor; a.save()
        messages.success(request,"Disponibilite ajoutee."); return redirect("manage_availability")
    return render(request,"doctors/availability.html",{"doctor":doctor,"availabilities":avails,"form":form})

@login_required
def delete_availability(request, availability_id):
    if request.user.role!="DOCTOR": return HttpResponseForbidden()
    doctor=get_object_or_404(Doctor,user=request.user)
    a=get_object_or_404(Availability,id=availability_id,doctor=doctor); a.delete()
    messages.success(request,"Disponibilite supprimee."); return redirect("manage_availability")
