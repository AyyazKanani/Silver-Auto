from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Part, Supplier, InventoryStock, PartSale

@login_required
def inventory_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    stocks = InventoryStock.objects.all()
    low_stock = [s for s in stocks if s.is_low_stock()]
    return render(request, 'admin/inventory.html', {'stocks': stocks, 'low_stock': low_stock})

@login_required
def parts_list(request):
    parts = Part.objects.all()
    return render(request, 'admin/parts.html', {'parts': parts})

@login_required
def add_part(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        Part.objects.create(
            part_name=request.POST['part_name'],
            vehicle_type=request.POST['vehicle_type'],
            price=request.POST['price'],
        )
        messages.success(request, 'Part added!')
        return redirect('parts_list')
    return render(request, 'admin/add_part.html')

@login_required
def supplier_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    suppliers = Supplier.objects.all()
    return render(request, 'admin/suppliers.html', {'suppliers': suppliers})

@login_required
def add_supplier(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        Supplier.objects.create(
            supplier_name=request.POST['supplier_name'],
            contact_number=request.POST['contact_number'],
            email=request.POST.get('email', ''),
            address=request.POST['address'],
        )
        messages.success(request, 'Supplier added!')
        return redirect('supplier_list')
    return render(request, 'admin/add_supplier.html')

@login_required
def update_stock(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        stock = get_object_or_404(InventoryStock, pk=pk)
        stock.quantity = request.POST['quantity']
        stock.save()
        messages.success(request, 'Stock updated!')
    return redirect('inventory_list')

@login_required
def sell_part(request):
    if request.method == 'POST':
        part_id = request.POST['part_id']
        quantity = int(request.POST['quantity'])
        part = get_object_or_404(Part, pk=part_id)
        stock = InventoryStock.objects.filter(part=part).first()
        if stock and stock.quantity >= quantity:
            stock.quantity -= quantity
            stock.save()
            PartSale.objects.create(
                part=part,
                quantity_sold=quantity,
                total_price=part.price * quantity,
                status='Completed'
            )
            messages.success(request, 'Part sold successfully!')
        else:
            messages.error(request, 'Insufficient stock!')
        return redirect('parts_list')
    parts = Part.objects.filter(status='Available')
    return render(request, 'admin/sell_part.html', {'parts': parts})