from django.urls import path
from . import views

urlpatterns = [
    # Path for the booking creation page
    path('create/', views.create_booking, name='create_booking'),
    # Path for the booking list (we'll create this view next)
    path('my-bookings/', views.booking_list, name='booking_list'),
    path('menu/', views.menu_view, name='menu'),
    path('edit/<int:pk>/', views.BookingUpdateView.as_view(), name='edit_booking'),
    path('delete/<int:pk>/', views.BookingDeleteView.as_view(),
         name='delete_booking'),
]
