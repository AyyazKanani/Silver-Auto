from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer, Mechanic, MechanicApplication, Driver, Attendance, SalaryPayment

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Redirect based on role
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif hasattr(user, 'mechanic'):
                return redirect('mechanic_dashboard')
            elif hasattr(user, 'driver'):
                return redirect('driver_dashboard')
            elif hasattr(user, 'customer'):
                return redirect('customer_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_customer(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        full_name = request.POST['full_name']
        mobile_number = request.POST['mobile_number']
        address = request.POST['address']
        city = request.POST.get('city', 'Ahmedabad')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')
        user = User.objects.create_user(username=username, password=password)
        Customer.objects.create(
            user=user, full_name=full_name,
            mobile_number=mobile_number, address=address, city=city
        )
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    return render(request, 'register.html')

def register_mechanic(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        full_name = request.POST['full_name']
        mobile_number = request.POST['mobile_number']
        address = request.POST['address']
        skills = request.POST['skills']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register_mechanic')
        user = User.objects.create_user(username=username, password=password)
        mechanic = Mechanic.objects.create(
            user=user, full_name=full_name,
            mobile_number=mobile_number, address=address,
            skills=skills, salary=0, account_status='Pending'
        )
        MechanicApplication.objects.create(mechanic=mechanic)
        messages.success(request, 'Application submitted! Wait for admin approval.')
        return redirect('login')
    return render(request, 'register_mechanic.html')

# ── ADMIN VIEWS ──
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    from service.models import ServiceRequest, Invoice
    from inventory.models import InventoryStock
    context = {
        'total_customers': Customer.objects.count(),
        'total_mechanics': Mechanic.objects.filter(account_status='Approved').count(),
        'pending_requests': ServiceRequest.objects.filter(service_status='Pending').count(),
        'total_requests': ServiceRequest.objects.count(),
        'low_stock': InventoryStock.objects.filter(quantity__lte=5).count(),
        'recent_requests': ServiceRequest.objects.order_by('-request_date')[:5],
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def manage_mechanics(request):
    if not request.user.is_superuser:
        return redirect('home')
    mechanics = Mechanic.objects.all()
    applications = MechanicApplication.objects.filter(status='Pending')
    return render(request, 'admin/mechanics.html', {'mechanics': mechanics, 'applications': applications})

@login_required
def approve_mechanic(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    action = request.POST.get('action')
    mechanic = get_object_or_404(Mechanic, pk=pk)
    app = MechanicApplication.objects.filter(mechanic=mechanic).last()
    if action == 'approve':
        mechanic.account_status = 'Approved'
        if app: app.status = 'Approved'
    else:
        mechanic.account_status = 'Rejected'
        if app: app.status = 'Rejected'
    mechanic.save()
    if app: app.save()
    messages.success(request, f'Mechanic {action}d successfully!')
    return redirect('manage_mechanics')

@login_required
def manage_customers(request):
    if not request.user.is_superuser:
        return redirect('home')
    customers = Customer.objects.all()
    return render(request, 'admin/customers.html', {'customers': customers})

@login_required
def manage_attendance(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        mechanic_id = request.POST['mechanic_id']
        date = request.POST['date']
        status = request.POST['status']
        mechanic = get_object_or_404(Mechanic, pk=mechanic_id)
        Attendance.objects.create(mechanic=mechanic, date=date, status=status)
        messages.success(request, 'Attendance marked!')
        return redirect('manage_attendance')
    mechanics = Mechanic.objects.filter(account_status='Approved')
    attendance = Attendance.objects.order_by('-date')[:20]
    return render(request, 'admin/attendance.html', {'mechanics': mechanics, 'attendance': attendance})

@login_required
def manage_salary(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        mechanic_id = request.POST['mechanic_id']
        month = request.POST['month']
        amount = request.POST['amount']
        payment_date = request.POST['payment_date']
        mechanic = get_object_or_404(Mechanic, pk=mechanic_id)
        SalaryPayment.objects.create(mechanic=mechanic, month=month, amount=amount, payment_date=payment_date)
        messages.success(request, 'Salary paid successfully!')
        return redirect('manage_salary')
    mechanics = Mechanic.objects.filter(account_status='Approved')
    salaries = SalaryPayment.objects.order_by('-payment_date')[:20]
    return render(request, 'admin/salary.html', {'mechanics': mechanics, 'salaries': salaries})

# ── CUSTOMER VIEWS ──
@login_required
def customer_dashboard(request):
    customer = get_object_or_404(Customer, user=request.user)
    from service.models import ServiceRequest
    from vehicles.models import Vehicle
    requests = ServiceRequest.objects.filter(customer=customer).order_by('-request_date')[:5]
    vehicles = Vehicle.objects.filter(customer=customer)
    return render(request, 'customer/dashboard.html', {'customer': customer, 'requests': requests, 'vehicles': vehicles})

# ── MECHANIC VIEWS ──
@login_required
def mechanic_dashboard(request):
    mechanic = get_object_or_404(Mechanic, user=request.user)
    from service.models import ServiceAssignment
    assignments = ServiceAssignment.objects.filter(mechanic=mechanic).order_by('-assigned_date')[:5]
    attendance = Attendance.objects.filter(mechanic=mechanic).order_by('-date')[:5]
    return render(request, 'mechanic/dashboard.html', {'mechanic': mechanic, 'assignments': assignments, 'attendance': attendance})

# ── DRIVER VIEWS ──
@login_required
def driver_dashboard(request):
    driver = get_object_or_404(Driver, user=request.user)
    from service.models import PickupDropRequest
    pickups = PickupDropRequest.objects.filter(driver=driver).order_by('-pickup_time')[:5]
    return render(request, 'driver/dashboard.html', {'driver': driver, 'pickups': pickups})

@login_required
def reports(request):
    if not request.user.is_superuser:
        return redirect('home')
    from service.models import ServiceRequest, Payment
    from inventory.models import InventoryStock
    completed = ServiceRequest.objects.filter(service_status='Completed')
    all_payments = Payment.objects.all()
    total_revenue = sum([p.invoice.grand_total for p in all_payments if p.payment_status == 'Success'])
    context = {
        'total_customers': Customer.objects.count(),
        'total_mechanics': Mechanic.objects.filter(account_status='Approved').count(),
        'completed_requests': completed.count(),
        'total_revenue': total_revenue,
        'all_requests': ServiceRequest.objects.all().order_by('-request_date'),
        'all_payments': all_payments,
        'all_stocks': InventoryStock.objects.all(),
    }
    return render(request, 'admin/reports.html', context)