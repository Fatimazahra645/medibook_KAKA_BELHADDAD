from django.contrib import admin
from .models import Doctor, Speciality, Availability

admin.site.register(Doctor)
admin.site.register(Speciality)
admin.site.register(Availability)