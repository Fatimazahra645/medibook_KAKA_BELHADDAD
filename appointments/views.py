from datetime import date as date_type
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from doctors.models import Doctor
from patients.models import Patient
from .models import Appointment, Consultation
from .forms import ConsultationForm
from .services import book_appointment, get_available_slots

@login_required
def book_appointment_view(request, doctor_id):
    if request.user.role!="PATIENT": return HttpResponseForbidden("Patients seulement.")
    try: patient=Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return render(request,"appointments/book.html",{"error":"Profil patient introuvable."})
    doctor=get_object_or_404(Doctor,pk=doctor_id,is_active=True)
    error=None; selected_date=None
    if request.method=="POST":
        ds=request.POST.get("date",""); ts=request.POST.get("time","")
        reason=request.POST.get("reason","").strip()
        if not ds or not ts or not reason: error="Veuillez remplir tous les champs."
        else:
            try:
                from datetime import datetime
                selected_date=datetime.strptime(ds,"%Y-%m-%d").date()
                selected_time=datetime.strptime(ts,"%H:%M").time()
                if selected_date<date_type.today(): error="Date dans le passe."
                else:
                    appt,msg=book_appointment(patient=patient,doctor=doctor,speciality=doctor.speciality,
                        date=selected_date,time=selected_time,reason=reason)
                    if appt:
                        try:
                            from notifications.models import Notification
                            Notification.objects.create(user=doctor.user,
                                message="Nouveau RDV: {} {} le {} a {}.".format(
                                    patient.user.first_name,patient.user.last_name,
                                    appt.date.strftime('%d/%m/%Y'),appt.time.strftime('%H:%M')),
                                notification_type="APPOINTMENT",appointment=appt)
                        except Exception: pass
                        return redirect("appointment_success")
                    else: error=msg
            except ValueError: error="Date ou heure invalide."
        if ds:
            try:
                from datetime import datetime
                selected_date=datetime.strptime(ds,"%Y-%m-%d").date()
            except ValueError: pass
    return render(request,"appointments/book.html",{"doctor":doctor,"error":error,
        "selected_date":selected_date.isoformat() if selected_date else "","today":date_type.today().isoformat()})

@login_required
def cancel_appointment_view(request, appointment_id):
    appt=get_object_or_404(Appointment,pk=appointment_id)
    if appt.patient.user!=request.user: return HttpResponseForbidden()
    if appt.status not in ["PENDING","CONFIRMED"]:
        messages.error(request,"Ce RDV ne peut plus etre annule."); return redirect("patient_dashboard")
    if request.method=="POST":
        appt.status="CANCELLED"; appt.save()
        try:
            from notifications.services import notify_doctor_cancellation
            notify_doctor_cancellation(appt)
        except Exception: pass
        messages.success(request,"Rendez-vous annule."); return redirect("patient_dashboard")
    return render(request,"appointments/cancel_confirm.html",{"appointment":appt})

@login_required
def reschedule_appointment_view(request, appointment_id):
    appt=get_object_or_404(Appointment,pk=appointment_id)
    if appt.patient.user!=request.user: return HttpResponseForbidden()
    if appt.status not in ["PENDING","CONFIRMED"]:
        messages.error(request,"Ce RDV ne peut plus etre modifie."); return redirect("patient_dashboard")
    doctor=appt.doctor; error=None; selected_date=None
    if request.method=="POST":
        ds=request.POST.get("date",""); ts=request.POST.get("time","")
        if not ds or not ts: error="Selectionnez date et creneau."
        else:
            try:
                from datetime import datetime
                selected_date=datetime.strptime(ds,"%Y-%m-%d").date()
                selected_time=datetime.strptime(ts,"%H:%M").time()
                if selected_date<date_type.today(): error="Date dans le passe."
                else:
                    slots=get_available_slots(doctor,selected_date,exclude_appointment_id=appt.pk)
                    if selected_time.strftime("%H:%M") not in slots: error="Creneau non disponible."
                    elif Appointment.objects.filter(doctor=doctor,date=selected_date,time=selected_time).exclude(pk=appt.pk).exists():
                        error="Creneau deja reserve."
                    else:
                        appt.date=selected_date; appt.time=selected_time; appt.status="PENDING"; appt.save()
                        try:
                            from notifications.services import notify_doctor_reschedule
                            notify_doctor_reschedule(appt)
                        except Exception: pass
                        messages.success(request,"RDV modifie."); return redirect("patient_dashboard")
            except ValueError: error="Date ou heure invalide."
        if ds:
            try:
                from datetime import datetime
                selected_date=datetime.strptime(ds,"%Y-%m-%d").date()
            except ValueError: pass
    return render(request,"appointments/reschedule.html",{"appointment":appt,"doctor":doctor,"error":error,
        "selected_date":selected_date.isoformat() if selected_date else "","today":date_type.today().isoformat()})

@login_required
def get_slots_view(request, doctor_id):
    doctor=get_object_or_404(Doctor,pk=doctor_id)
    ds=request.GET.get("date",""); excl=request.GET.get("exclude")
    if not ds: return JsonResponse({"slots":[]})
    try:
        from datetime import datetime
        target=datetime.strptime(ds,"%Y-%m-%d").date()
        e=int(excl) if excl else None
        return JsonResponse({"slots":get_available_slots(doctor,target,exclude_appointment_id=e)})
    except (ValueError,TypeError): return JsonResponse({"slots":[],"error":"Date invalide"})

@login_required
def appointment_success_view(request):
    return render(request,"appointments/success.html")

@login_required
def create_consultation_view(request, appointment_id):
    appt=get_object_or_404(Appointment,pk=appointment_id)
    if appt.doctor.user!=request.user: return HttpResponseForbidden()
    if hasattr(appt,'consultation'):
        messages.info(request,"Consultation deja creee."); return redirect("doctor_dashboard")
    if request.method=="POST":
        form=ConsultationForm(request.POST)
        if form.is_valid():
            c=form.save(commit=False); c.appointment=appt; c.save()
            appt.status="COMPLETED"; appt.save()
            messages.success(request,"Consultation enregistree."); return redirect("doctor_dashboard")
    else: form=ConsultationForm()
    return render(request,"appointments/create_consultation.html",{"form":form,"appointment":appt})

@login_required
def confirm_appointment_view(request, appointment_id):
    if request.method!="POST": return redirect("doctor_dashboard")
    appt=get_object_or_404(Appointment,pk=appointment_id)
    if appt.doctor.user!=request.user: return HttpResponseForbidden()
    if appt.status!="PENDING":
        messages.error(request,"Ce RDV ne peut pas etre confirme."); return redirect("doctor_dashboard")
    appt.status="CONFIRMED"; appt.save()
    try:
        from notifications.models import Notification
        Notification.objects.create(user=appt.patient.user,
            message="Votre RDV du {} a {} avec Dr. {} a ete confirme.".format(
                appt.date.strftime('%d/%m/%Y'),appt.time.strftime('%H:%M'),appt.doctor.user.last_name),
            notification_type="APPOINTMENT",appointment=appt)
    except Exception: pass
    messages.success(request,"RDV confirme."); return redirect("doctor_dashboard")

@login_required
def doctor_cancel_appointment_view(request, appointment_id):
    if request.method!="POST": return redirect("doctor_dashboard")
    appt=get_object_or_404(Appointment,pk=appointment_id)
    if appt.doctor.user!=request.user: return HttpResponseForbidden()
    if appt.status not in ["PENDING","CONFIRMED"]:
        messages.error(request,"Ce RDV ne peut plus etre annule."); return redirect("doctor_dashboard")
    appt.status="CANCELLED"; appt.save()
    try:
        from notifications.models import Notification
        Notification.objects.create(user=appt.patient.user,
            message="Votre RDV du {} a {} a ete annule par Dr. {}.".format(
                appt.date.strftime('%d/%m/%Y'),appt.time.strftime('%H:%M'),appt.doctor.user.last_name),
            notification_type="APPOINTMENT",appointment=appt)
    except Exception: pass
    messages.success(request,"RDV annule."); return redirect("doctor_dashboard")

@login_required
def mark_absent_view(request, appointment_id):
    if request.method!="POST": return redirect("doctor_dashboard")
    appt=get_object_or_404(Appointment,pk=appointment_id)
    if appt.doctor.user!=request.user: return HttpResponseForbidden()
    appt.status="ABSENT"; appt.save()
    messages.success(request,"Patient marque absent."); return redirect("doctor_dashboard")
