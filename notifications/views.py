from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
@login_required
def notifications_list(request):
    notifs=Notification.objects.filter(user=request.user).order_by("-created_at")[:50]
    Notification.objects.filter(user=request.user,is_read=False).update(is_read=True)
    return render(request,"notifications/list.html",{"notifications":notifs})
