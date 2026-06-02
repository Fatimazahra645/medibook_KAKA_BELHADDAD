from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from patients.models import Patient
from appointments.models import Appointment
from doctors.models import Doctor

@staff_member_required
def admin_dashboard(request):
    by_spec=Appointment.objects.values("speciality__name").annotate(count=Count("id")).order_by("-count")[:10]
    top_docs=Doctor.objects.annotate(cnt=Count("appointment")).order_by("-cnt").select_related("user","speciality")[:5]
    return render(request,"dashboard/admin_dashboard.html",{
        "total_patients":Patient.objects.count(),"total_doctors":Doctor.objects.count(),
        "total_appointments":Appointment.objects.count(),
        "pending_count":Appointment.objects.filter(status="PENDING").count(),
        "confirmed_count":Appointment.objects.filter(status="CONFIRMED").count(),
        "cancelled_count":Appointment.objects.filter(status="CANCELLED").count(),
        "completed_count":Appointment.objects.filter(status="COMPLETED").count(),
        "absent_count":Appointment.objects.filter(status="ABSENT").count(),
        "appts_by_spec":by_spec,"top_docs":top_docs})

@login_required
def doctor_dashboard(request):
    if request.user.role!="DOCTOR": return HttpResponseForbidden()
    doctor=get_object_or_404(Doctor,user=request.user)
    today=timezone.now().date(); week_end=today+timedelta(days=7)
    today_appts=Appointment.objects.filter(doctor=doctor,date=today).select_related("patient__user").order_by("time")
    week_appts=Appointment.objects.filter(doctor=doctor,date__range=[today,week_end]).select_related("patient__user").order_by("date","time")
    try:
        from notifications.models import Notification
        notifs=list(Notification.objects.filter(user=request.user,is_read=False))
        Notification.objects.filter(user=request.user,is_read=False).update(is_read=True)
    except Exception: notifs=[]
    return render(request,"dashboard/doctor_dashboard.html",{
        "doctor":doctor,"today_appointments":today_appts,"week_appointments":week_appts,
        "total_appointments":Appointment.objects.filter(doctor=doctor).count(),
        "confirmed_count":Appointment.objects.filter(doctor=doctor,status="CONFIRMED").count(),
        "cancelled_count":Appointment.objects.filter(doctor=doctor,status="CANCELLED").count(),
        "completed_count":Appointment.objects.filter(doctor=doctor,status="COMPLETED").count(),
        "pending_count":Appointment.objects.filter(doctor=doctor,status="PENDING").count(),
        "unread_notifications":notifs,"today":today})

@login_required
def patient_dashboard(request):
    if request.user.role!="PATIENT": return HttpResponseForbidden()
    patient=get_object_or_404(Patient,user=request.user)
    upcoming=Appointment.objects.filter(patient=patient,status__in=["PENDING","CONFIRMED"]).order_by("date","time").select_related("doctor__user","speciality")
    past=Appointment.objects.filter(patient=patient,status__in=["COMPLETED","ABSENT"]).order_by("-date").select_related("doctor__user","speciality")
    cancelled=Appointment.objects.filter(patient=patient,status="CANCELLED").order_by("-date").select_related("doctor__user","speciality")
    try:
        from notifications.models import Notification
        notifs=list(Notification.objects.filter(user=request.user,is_read=False)[:5])
    except Exception: notifs=[]
    return render(request,"dashboard/patient_dashboard.html",{
        "patient":patient,"upcoming_appointments":upcoming,
        "past_appointments":past,"cancelled_appointments":cancelled,"notifications":notifs})
