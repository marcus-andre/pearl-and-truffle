from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking

# Create your views here.


@login_required
def create_booking(request):
    """
    View to handle the creation of a new booking.
    It checks if the request is a POST (form submission) or GET (viewing the page).
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Create booking instance but don't save to DB yet
            booking = form.save(commit=False)
            # Link the booking to the currently logged-in user
            booking.user = request.user
            booking.save()
            # AC3: Show success message upon successful reservation
            messages.success(request, 'Your booking has been successful!')
            return redirect('booking_list')
    else:
        # If it's a GET request, create an empty form
        form = BookingForm()

    context = {
        'form': form
    }
    return render(request, 'booking/create_booking.html', context)


@login_required
def booking_list(request):
    """
    View to display a list of bookings for the logged-in user.
    """
    # Fetch only the bookings belonging to the current user, ordered by date
    bookings = Booking.objects.filter(
        user=request.user).order_by('booking_date')

    return render(request, 'booking/booking_list.html', {'bookings': bookings})
