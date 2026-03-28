from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    price_per_day = models.IntegerField()

    image = models.ImageField(upload_to='cars/', blank=True, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    total_amount = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.car.name}"