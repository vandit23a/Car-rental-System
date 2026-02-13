from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('bill/<int:booking_id>/', views.bill, name='bill'),
]
