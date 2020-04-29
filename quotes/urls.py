from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about.html', views.about, name='about'),
    path('update_stock.html', views.update_stock, name='update_stock'),
    path('delete/<stock_id>', views.delete, name='delete'),
    path('lookup_stock.html', views.lookup_stock, name='lookup_stock'),      
]