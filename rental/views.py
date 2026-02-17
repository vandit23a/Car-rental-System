from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from datetime import date

# temporary import (we will create models later)
# comment if models not created yet
try:
    from .models import Car, Booking
except:
    Car = None
    Booking = None


# HOME PAGE
def home(request):
    cars = Car.objects.all() if Car else []
    return render(request, 'home.html', {'cars': cars})


# DASHBOARD
@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user) if Booking else []
    return render(request, 'dashboard.html', {'bookings': bookings})


# BOOK CAR
@login_required
def book_car(request, car_id):

    if not Car:
        return render(request, 'error.html')

    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":

        start = request.POST['start_date']
        end = request.POST['end_date']

        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)

        today = date.today()

        # validation
        if start_date < today:

            return render(request, 'book.html',
            {'car': car, 'error': 'Past date not allowed'})

        duration = (end_date - start_date).days

        if duration > 30:

            return render(request, 'book.html',
            {'car': car, 'error': 'Max 30 days allowed'})


        total = duration * car.price_per_day

        booking = Booking.objects.create(

            user=request.user,
            car=car,
            start_date=start_date,
            end_date=end_date,
            total_amount=total

        )

        return redirect('bill', booking_id=booking.id)

    return render(request, 'book.html', {'car': car})


# BILL
@login_required
def bill(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)

    return render(request, 'bill.html', {'booking': booking})


# REGISTER
def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('dashboard')

    else:

        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
