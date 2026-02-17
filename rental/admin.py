from django.contrib import admin

from .models import Category, Car, Booking

admin.site.register(Category)

admin.site.register(Car)

admin.site.register(Booking)