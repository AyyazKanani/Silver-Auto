from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=50, default='Ahmedabad')
    status = models.CharField(max_length=20, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Mechanic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    skills = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    account_status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class MechanicApplication(models.Model):
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    apply_date = models.DateField(auto_now_add=True)
    STATUS = [('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected')]
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')

    def __str__(self):
        return f"{self.mechanic.full_name} - {self.status}"

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return self.full_name

class Attendance(models.Model):
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    date = models.DateField()
    STATUS = [('Present','Present'),('Absent','Absent')]
    status = models.CharField(max_length=20, choices=STATUS)
    remarks = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.mechanic.full_name} - {self.date} - {self.status}"

class SalaryPayment(models.Model):
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"{self.mechanic.full_name} - {self.month}"

class Notification(models.Model):
    ROLE_CHOICES = [
        ('Customer','Customer'),
        ('Mechanic','Mechanic'),
        ('Admin','Admin'),
        ('Driver','Driver')
    ]
    receiver_role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    receiver_id = models.IntegerField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receiver_role} - {self.message[:30]}"