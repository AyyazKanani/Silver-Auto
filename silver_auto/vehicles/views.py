from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehicle, VehicleType
from accounts.models import Customer

@login_required
def my_vehicles(request):
    customer = get_object_or_404(Customer, user=request.user)
    vehicles = Vehicle.objects.filter(customer=customer)
    return render(request, 'customer/my_vehicles.html', {'vehicles': vehicles})

@login_required
def add_vehicle(request):
    customer = get_object_or_404(Customer, user=request.user)
    if request.method == 'POST':
        vehicle_type = get_object_or_404(VehicleType, pk=request.POST['vehicle_type_id'])
        Vehicle.objects.create(
            customer=customer,
            vehicle_number=request.POST['vehicle_number'],
            vehicle_type=vehicle_type,
            brand=request.POST['brand'],
            model=request.POST['model'],
            registration_year=request.POST['registration_year'],
        )
        messages.success(request, 'Vehicle added!')
        return redirect('my_vehicles')
    vehicle_types = VehicleType.objects.all()
    return render(request, 'customer/add_vehicle.html', {'vehicle_types': vehicle_types})

@login_required
def all_vehicles(request):
    if not request.user.is_superuser:
        return redirect('home')
    vehicles = Vehicle.objects.all()
    return render(request, 'admin/all_vehicles.html', {'vehicles': vehicles})