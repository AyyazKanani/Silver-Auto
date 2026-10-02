from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from accounts.models import Customer, Mechanic, Driver
from vehicles.models import Vehicle

class ServicePrice(models.Model):
    service_type = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=30)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    additional_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.service_type} - {self.vehicle_type} - Rs.{self.final_price}"

class ServiceRequest(models.Model):
    STATUS = [
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
        ('In Progress','In Progress'),
        ('Completed','Completed'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    problem_description = models.TextField()
    service_status = models.CharField(max_length=30, choices=STATUS, default='Pending')
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    request_date = models.DateField(auto_now_add=True)
    preferred_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Request #{self.id} - {self.customer.full_name} - {self.service_status}"

class ServiceAssignment(models.Model):
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Assignment #{self.id} - {self.mechanic.full_name}"

class ServiceRepair(models.Model):
    STATUS = [('In Progress','In Progress'),('Completed','Completed')]
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    repair_notes = models.TextField()
    labor_hours = models.IntegerField(default=0)
    repair_status = models.CharField(max_length=20, choices=STATUS, default='In Progress')

    def __str__(self):
        return f"Repair #{self.id} - {self.repair_status}"

class PickupDropRequest(models.Model):
    STATUS = [
        ('Scheduled','Scheduled'),
        ('Picked Up','Picked Up'),
        ('Dropped','Dropped'),
    ]
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    pickup_address = models.TextField()
    drop_address = models.TextField(default='Silver Auto, Vatva, Ahmedabad')
    pickup_time = models.DateTimeField()
    drop_time = models.DateTimeField(null=True, blank=True)
    pickup_status = models.CharField(max_length=20, choices=STATUS, default='Scheduled')
    vehicle_condition_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pickup #{self.id} - {self.pickup_status}"

class Invoice(models.Model):
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    invoice_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice #{self.id} - Rs.{self.grand_total}"

class Payment(models.Model):
    METHOD = [('Cash','Cash'),('UPI','UPI'),('Card','Card')]
    STATUS = [('Success','Success'),('Failed','Failed'),('Pending','Pending')]
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=30, choices=METHOD)
    payment_status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.payment_method} - {self.payment_status}"

class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    message = models.TextField()
    feedback_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.customer.full_name} - {self.rating} stars"
