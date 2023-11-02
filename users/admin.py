from django.contrib import admin
from .models import Admin, Doctor, Appointment, Secretary


# Register your models here.

admin.site.register(Admin)

admin.site.register(Doctor)

admin.site.register(Secretary)

admin.site.register(Appointment)