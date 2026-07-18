from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_vehicles, name='my_vehicles'),
    path('add/', views.add_vehicle, name='add_vehicle'),
    path('all/', views.all_vehicles, name='all_vehicles'),
]