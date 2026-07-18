from django.urls import path
from . import views

urlpatterns = [
    # Service Request
    path('request/', views.create_request, name='create_request'),
    path('requests/', views.my_requests, name='my_requests'),
    path('requests/all/', views.all_requests, name='all_requests'),
    path('request/approve/<int:pk>/', views.approve_request, name='approve_request'),
    path('request/reject/<int:pk>/', views.reject_request, name='reject_request'),
    path('request/assign/<int:pk>/', views.assign_mechanic, name='assign_mechanic'),

    # Pickup Drop
    path('pickup/request/<int:pk>/', views.request_pickup, name='request_pickup'),
    path('pickup/all/', views.all_pickups, name='all_pickups'),
    path('pickup/update/<int:pk>/', views.update_pickup, name='update_pickup'),

    # Invoice & Payment
    path('invoice/<int:pk>/', views.view_invoice, name='view_invoice'),
    path('invoice/create/<int:pk>/', views.create_invoice, name='create_invoice'),
    path('payment/<int:pk>/', views.make_payment, name='make_payment'),

    # Feedback
    path('feedback/<int:pk>/', views.submit_feedback, name='submit_feedback'),
    path('feedback/all/', views.all_feedback, name='all_feedback'),

    # Mechanic jobs
    path('jobs/', views.mechanic_jobs, name='mechanic_jobs'),
    path('jobs/update/<int:pk>/', views.update_job, name='update_job'),
]