from django.urls import path
from apps.tickets.views import UserTicketListView, UserTicketDetailView

urlpatterns = [
    path('', UserTicketListView.as_view(), name='tickets-list'),
    path('<int:pk>/', UserTicketDetailView.as_view(), name='tickets-detail'),
]