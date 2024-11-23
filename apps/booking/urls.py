from django.urls import path
from apps.booking.views import BookingDetailView, BookingListView, BookingPDFDownloadView

urlpatterns = [
    path('', BookingListView.as_view(), name='booking-list'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('download/<int:pk>/pdf', BookingPDFDownloadView.as_view(), name='booking-pdf-download'),
]
