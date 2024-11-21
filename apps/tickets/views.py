from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import transaction

from apps.tickets.models import UserTicket
from apps.tickets.serializers import UserTicketSerializer
from utils.response import CustomResponse


class UserTicketListView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['booking', 'status']
    search_fields = ['user_name', 'contact']

    def get(self, request):
        # If admin, show all tickets; otherwise, show tickets from user's bookings
        if request.user.is_staff:
            queryset = UserTicket.objects.all()
        else:
            queryset = UserTicket.objects.filter(booking__user=request.user)

        serializer = UserTicketSerializer(queryset, many=True)
        return CustomResponse.success(
            message="User tickets retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    @transaction.atomic
    def post(self, request):
        serializer = UserTicketSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Additional checks can be added here
            ticket = serializer.save()
            return CustomResponse.success(
                message="User ticket created successfully",
                data=UserTicketSerializer(ticket).data,
                status_code=status.HTTP_201_CREATED
            )


class UserTicketDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            ticket = UserTicket.objects.get(pk=pk)
            # Ensure user can only access their own tickets or admin can access all
            if not user.is_staff and ticket.booking.user != user:
                return None
            return ticket
        except UserTicket.DoesNotExist:
            return None

    def get(self, request, pk):
        instance = self.get_object(pk, request.user)
        if not instance:
            return CustomResponse.error(
                message="User ticket not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = UserTicketSerializer(instance)
        return CustomResponse.success(
            message="User ticket retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    @transaction.atomic
    def put(self, request, pk):
        instance = self.get_object(pk, request.user)
        if not instance:
            return CustomResponse.error(
                message="User ticket not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Prevent modifying booked tickets
        if instance.status == 'booked':
            return CustomResponse.error(
                message="Cannot modify a booked ticket",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserTicketSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            ticket = serializer.save()
            return CustomResponse.success(
                message="User ticket updated successfully",
                data=UserTicketSerializer(ticket).data,
                status_code=status.HTTP_200_OK
            )

    @transaction.atomic
    def delete(self, request, pk):
        instance = self.get_object(pk, request.user)
        if not instance:
            return CustomResponse.error(
                message="User ticket not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Prevent deleting booked tickets
        if instance.status == 'booked':
            return CustomResponse.error(
                message="Cannot delete a booked ticket",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        instance.delete()
        return CustomResponse.success(
            message="User ticket deleted successfully",
            status_code=status.HTTP_200_OK
        )
