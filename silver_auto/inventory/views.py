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
        part_name = request.POST.get('part_name', '').strip()
        vehicle_type = request.POST.get('vehicle_type', '').strip()
        price = request.POST.get('price')
        if not part_name or not vehicle_type or not price:
            messages.error(request, 'Please fill in all part fields.')
            return render(request, 'admin/add_part.html')
        try:
            price_value = float(price)
            if price_value <= 0:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid positive price.')
            return render(request, 'admin/add_part.html')
        Part.objects.create(
            part_name=part_name,
            vehicle_type=vehicle_type,
            price=price_value,
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
        supplier_name = request.POST.get('supplier_name', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        if not supplier_name or not contact_number or not address:
            messages.error(request, 'Please fill in all required supplier fields.')
            return render(request, 'admin/add_supplier.html')
        Supplier.objects.create(
            supplier_name=supplier_name,
            contact_number=contact_number,
            email=email,
            address=address,
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
        try:
            quantity = int(request.POST.get('quantity', 0))
            if quantity < 0:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid non-negative quantity.')
            return redirect('inventory_list')
        stock.quantity = quantity
        stock.save()
        messages.success(request, 'Stock updated!')
    return redirect('inventory_list')

@login_required
def sell_part(request):
    if request.method == 'POST':
        part_id = request.POST.get('part_id')
        try:
            quantity = int(request.POST.get('quantity', 0))
            if quantity <= 0:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid positive quantity.')
            return redirect('parts_list')
        if not part_id:
            messages.error(request, 'Please select a part.')
            return redirect('parts_list')
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