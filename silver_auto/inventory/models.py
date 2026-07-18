from django.db import models

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return self.supplier_name

class Part(models.Model):
    STATUS = [('Available','Available'),('Out of Stock','Out of Stock')]
    part_name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default='Available')

    def __str__(self):
        return f"{self.part_name} - {self.vehicle_type}"

class InventoryStock(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=5)
    last_updated = models.DateTimeField(auto_now=True)

    def is_low_stock(self):
        return self.quantity <= self.reorder_level

    def __str__(self):
        return f"{self.part.part_name} - Qty: {self.quantity}"

class PartSale(models.Model):
    STATUS = [('Pending','Pending'),('Completed','Completed'),('Cancelled','Cancelled')]
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')

    def __str__(self):
        return f"Sale #{self.id} - {self.part.part_name} x{self.quantity_sold}"