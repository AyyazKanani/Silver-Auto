from django.db import models
from accounts.models import Customer

class VehicleType(models.Model):
    type_name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.type_name

class Vehicle(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    registration_year = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.vehicle_number}"