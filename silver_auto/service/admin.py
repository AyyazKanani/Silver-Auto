from django.contrib import admin
from .models import ServiceRequest, ServiceAssignment, ServiceRepair, ServicePrice, PickupDropRequest, Invoice, Payment, Feedback

admin.site.register(ServiceRequest)
admin.site.register(ServiceAssignment)
admin.site.register(ServiceRepair)
admin.site.register(ServicePrice)
admin.site.register(PickupDropRequest)
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Feedback)