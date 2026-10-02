from django.db import IntegrityError
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
        vehicle_type_id = request.POST.get('vehicle_type_id')
        vehicle_number = request.POST.get('vehicle_number', '').strip()
        brand = request.POST.get('brand', '').strip()
        model = request.POST.get('model', '').strip()
        registration_year = request.POST.get('registration_year')
        if not vehicle_type_id or not vehicle_number or not brand or not model or not registration_year:
            messages.error(request, 'Please fill in all vehicle fields.')
            return redirect('add_vehicle')
        try:
            registration_year = int(registration_year)
            if registration_year < 1980 or registration_year > 2030:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid registration year.')
            return redirect('add_vehicle')
        vehicle_type = get_object_or_404(VehicleType, pk=vehicle_type_id)
        try:
            Vehicle.objects.create(
                customer=customer,
                vehicle_number=vehicle_number,
                vehicle_type=vehicle_type,
                brand=brand,
                model=model,
                registration_year=registration_year,
            )
        except IntegrityError:
            messages.error(request, 'This vehicle number is already registered!')
            return redirect('add_vehicle')
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