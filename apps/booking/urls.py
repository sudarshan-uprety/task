from django.urls import path
from apps.booking.views import BookingDetailView, BookingListView

urlpatterns = [
    path('', BookingListView.as_view(), name='booking-list'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
]