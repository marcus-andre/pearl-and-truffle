from django.urls import path
from . import views

urlpatterns = [
    # Path for the booking creation page
    path('create/', views.create_booking, name='create_booking'),
    # Path for the booking list (we'll create this view next)
    path('my-bookings/', views.booking_list, name='booking_list'),
]
