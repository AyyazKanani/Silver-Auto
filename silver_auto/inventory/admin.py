from django.contrib import admin
from .models import Part, Supplier, InventoryStock, PartSale

admin.site.register(Part)
admin.site.register(Supplier)
admin.site.register(InventoryStock)