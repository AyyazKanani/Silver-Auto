from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('parts/', views.parts_list, name='parts_list'),
    path('parts/add/', views.add_part, name='add_part'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('stock/update/<int:pk>/', views.update_stock, name='update_stock'),
    path('parts/sell/', views.sell_part, name='sell_part'),
]