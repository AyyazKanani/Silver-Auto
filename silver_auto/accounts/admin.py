from django.contrib import admin
from .models import Customer, Mechanic, MechanicApplication, Driver, Attendance, SalaryPayment, Notification

admin.site.register(Customer)
admin.site.register(Mechanic)
admin.site.register(MechanicApplication)
admin.site.register(Driver)
admin.site.register(Attendance)
admin.site.register(SalaryPayment)
admin.site.register(Notification)