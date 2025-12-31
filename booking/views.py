from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import BookingForm
from .models import Booking

# --- Function-Based Views ---


def home_page(request):
    """
    Display the restaurant's home page.
    """
    return render(request, "index.html")


def menu_view(request):
    """
    Display the restaurant's menu.
    """
    return render(request, 'menu.html')


@login_required
def create_booking(request):
    """
    View to handle the creation of a new booking.
    Links the booking to the currently logged-in user.
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Your booking has been successful!')
            return redirect('booking_list')
    else:
        form = BookingForm()

    return render(request, 'booking/create_booking.html', {'form': form})


@login_required
def booking_list(request):
    """
    View to display a list of bookings for the logged-in user.
    AC1 & AC2: Only bookings belonging to the current user are shown.
    """
    bookings = Booking.objects.filter(
        user=request.user).order_by('booking_date')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

# --- Class-Based Views for Management ---


class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    AC3: View to allow users to update their own bookings.
    Uses UserPassesTestMixin for security.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'booking/edit_booking.html'
    success_url = reverse_lazy('booking_list')

    def form_valid(self, form):
        # Show success message upon successful update
        messages.success(
            self.request, "Your booking was successfully updated.")
        return super().form_valid(form)

    def test_func(self):
        # Security: Ensure only the booking owner can edit it
        booking = self.get_object()
        return self.request.user == booking.user


class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    AC4 & AC5: View to handle booking cancellation.
    Provides a confirmation page before deletion.
    """
    model = Booking
    template_name = 'booking/confirm_delete.html'
    success_url = reverse_lazy('booking_list')

    def delete(self, request, *args, **kwargs):
        # Show success message upon cancellation
        messages.success(self.request, "Your booking has been cancelled.")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        # Security: Ensure only the booking owner can delete it
        booking = self.get_object()
        return self.request.user == booking.user
