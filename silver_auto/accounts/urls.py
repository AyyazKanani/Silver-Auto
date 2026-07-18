from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_customer, name='register'),

    # Admin URLs
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/mechanics/', views.manage_mechanics, name='manage_mechanics'),
    path('dashboard/admin/mechanics/approve/<int:pk>/', views.approve_mechanic, name='approve_mechanic'),
    path('dashboard/admin/customers/', views.manage_customers, name='manage_customers'),
    path('dashboard/admin/attendance/', views.manage_attendance, name='manage_attendance'),
    path('dashboard/admin/salary/', views.manage_salary, name='manage_salary'),

    # Customer URLs
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),

    # Mechanic URLs
    path('dashboard/mechanic/', views.mechanic_dashboard, name='mechanic_dashboard'),

    # Driver URLs
    path('dashboard/driver/', views.driver_dashboard, name='driver_dashboard'),
    path('dashboard/admin/reports/', views.reports, name='reports'),
]