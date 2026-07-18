from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServiceRequest, ServiceAssignment, ServiceRepair, ServicePrice, PickupDropRequest, Invoice, Payment, Feedback
from accounts.models import Customer, Mechanic, Driver
from vehicles.models import Vehicle

@login_required
def create_request(request):
    customer = get_object_or_404(Customer, user=request.user)
    if request.method == 'POST':
        vehicle_id = request.POST['vehicle_id']
        problem_description = request.POST['problem_description']
        preferred_date = request.POST['preferred_date']
        service_type = request.POST.get('service_type', '')
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        price = ServicePrice.objects.filter(
            service_type=service_type,
            vehicle_type=vehicle.vehicle_type.type_name
        ).first()
        estimated_price = price.final_price if price else 0
        ServiceRequest.objects.create(
            customer=customer, vehicle=vehicle,
            problem_description=problem_description,
            preferred_date=preferred_date,
            estimated_price=estimated_price
        )
        messages.success(request, 'Service request submitted successfully!')
        return redirect('my_requests')
    vehicles = Vehicle.objects.filter(customer=customer)
    service_prices = ServicePrice.objects.filter(status='Active')
    return render(request, 'customer/create_request.html', {'vehicles': vehicles, 'service_prices': service_prices})

@login_required
def my_requests(request):
    customer = get_object_or_404(Customer, user=request.user)
    requests = ServiceRequest.objects.filter(customer=customer).order_by('-request_date')
    return render(request, 'customer/my_requests.html', {'requests': requests})

@login_required
def all_requests(request):
    if not request.user.is_superuser:
        return redirect('home')
    requests = ServiceRequest.objects.all().order_by('-request_date')
    mechanics = Mechanic.objects.filter(account_status='Approved')
    return render(request, 'admin/all_requests.html', {'requests': requests, 'mechanics': mechanics})

@login_required
def approve_request(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    req = get_object_or_404(ServiceRequest, pk=pk)
    req.service_status = 'Approved'
    req.save()
    messages.success(request, 'Request approved!')
    return redirect('all_requests')

@login_required
def reject_request(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    req = get_object_or_404(ServiceRequest, pk=pk)
    req.service_status = 'Rejected'
    req.save()
    messages.success(request, 'Request rejected!')
    return redirect('all_requests')

@login_required
def assign_mechanic(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        mechanic_id = request.POST['mechanic_id']
        req = get_object_or_404(ServiceRequest, pk=pk)
        mechanic = get_object_or_404(Mechanic, pk=mechanic_id)
        ServiceAssignment.objects.create(request=req, mechanic=mechanic)
        req.service_status = 'In Progress'
        req.save()
        messages.success(request, 'Mechanic assigned!')
    return redirect('all_requests')

@login_required
def mechanic_jobs(request):
    mechanic = get_object_or_404(Mechanic, user=request.user)
    assignments = ServiceAssignment.objects.filter(mechanic=mechanic).order_by('-assigned_date')
    return render(request, 'mechanic/jobs.html', {'assignments': assignments})

@login_required
def update_job(request, pk):
    mechanic = get_object_or_404(Mechanic, user=request.user)
    if request.method == 'POST':
        assignment = get_object_or_404(ServiceAssignment, pk=pk, mechanic=mechanic)
        status = request.POST['status']
        notes = request.POST.get('notes', '')
        repair, created = ServiceRepair.objects.get_or_create(request=assignment.request)
        repair.repair_notes = notes
        repair.repair_status = status
        repair.save()
        if status == 'Completed':
            assignment.request.service_status = 'Completed'
            assignment.request.save()
        messages.success(request, 'Job updated!')
    return redirect('mechanic_jobs')

@login_required
def request_pickup(request, pk):
    customer = get_object_or_404(Customer, user=request.user)
    service_req = get_object_or_404(ServiceRequest, pk=pk, customer=customer)
    if request.method == 'POST':
        pickup_address = request.POST['pickup_address']
        pickup_time = request.POST['pickup_time']
        PickupDropRequest.objects.create(
            request=service_req,
            pickup_address=pickup_address,
            pickup_time=pickup_time
        )
        messages.success(request, 'Pickup request submitted!')
        return redirect('my_requests')
    return render(request, 'customer/request_pickup.html', {'service_req': service_req})

@login_required
def all_pickups(request):
    if not request.user.is_superuser:
        return redirect('home')
    pickups = PickupDropRequest.objects.all().order_by('-pickup_time')
    drivers = Driver.objects.filter(status='Active')
    return render(request, 'admin/all_pickups.html', {'pickups': pickups, 'drivers': drivers})

@login_required
def update_pickup(request, pk):
    if request.method == 'POST':
        pickup = get_object_or_404(PickupDropRequest, pk=pk)
        status = request.POST.get('status')
        driver_id = request.POST.get('driver_id')
        if driver_id:
            pickup.driver = get_object_or_404(Driver, pk=driver_id)
        if status:
            pickup.pickup_status = status
        pickup.save()
        messages.success(request, 'Pickup updated!')
    return redirect('all_pickups')

@login_required
def create_invoice(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    service_req = get_object_or_404(ServiceRequest, pk=pk)
    if request.method == 'POST':
        total_amount = float(request.POST['total_amount'])
        tax_amount = round(total_amount * 0.18, 2)
        grand_total = total_amount + tax_amount
        Invoice.objects.create(
            request=service_req,
            total_amount=total_amount,
            tax_amount=tax_amount,
            grand_total=grand_total
        )
        messages.success(request, 'Invoice created!')
        return redirect('all_requests')
    return render(request, 'admin/create_invoice.html', {'service_req': service_req})

@login_required
def view_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    payment = Payment.objects.filter(invoice=invoice).first()
    return render(request, 'customer/invoice.html', {'invoice': invoice, 'payment': payment})

@login_required
def make_payment(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        method = request.POST['payment_method']
        Payment.objects.create(invoice=invoice, payment_method=method, payment_status='Success')
        messages.success(request, 'Payment successful!')
        return redirect('my_requests')
    return render(request, 'customer/payment.html', {'invoice': invoice})

@login_required
def submit_feedback(request, pk):
    customer = get_object_or_404(Customer, user=request.user)
    service_req = get_object_or_404(ServiceRequest, pk=pk, customer=customer)
    if request.method == 'POST':
        rating = request.POST['rating']
        message = request.POST['message']
        Feedback.objects.create(
            customer=customer, request=service_req,
            rating=rating, message=message
        )
        messages.success(request, 'Feedback submitted!')
        return redirect('my_requests')
    return render(request, 'customer/feedback.html', {'service_req': service_req})

@login_required
def all_feedback(request):
    if not request.user.is_superuser:
        return redirect('home')
    feedbacks = Feedback.objects.all().order_by('-feedback_date')
    return render(request, 'admin/all_feedback.html', {'feedbacks': feedbacks})