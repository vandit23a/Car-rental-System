from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q

from .models import Car, Booking
from .forms import SimpleRegisterForm


@login_required
def home(request):
    cars = Car.objects.all()
    return render(request, 'home.html', {'cars': cars})


@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'bookings': bookings})


@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')

        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
        today = date.today()

        if start_date < today:
            return render(request, 'book.html', {'car': car, 'error': 'Past date not allowed'})

        if end_date <= start_date:
            return render(request, 'book.html', {'car': car, 'error': 'End date must be after start date'})

        duration = (end_date - start_date).days

        if duration > 30:
            return render(request, 'book.html', {'car': car, 'error': 'Max 30 days allowed'})

        overlapping_booking = Booking.objects.filter(
            car=car
        ).filter(
            Q(start_date__lt=end_date) & Q(end_date__gt=start_date)
        ).exists()

        if overlapping_booking:
            return render(request, 'book.html', {'car': car, 'error': 'This car is already booked for selected dates'})

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


@login_required
def bill(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bill.html', {'booking': booking})


def register(request):
    if request.method == 'POST':
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/home/')
    else:
        form = SimpleRegisterForm()

    return render(request, 'register.html', {'form': form})