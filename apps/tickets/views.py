from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import transaction

from apps.tickets.models import UserTicket
from apps.tickets.serializers import UserTicketRetrieveSerializer, UserTicketCreateSerializer, UserTicketUpdateSerializer
from utils.response import CustomResponse


class UserTicketListView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['booking', 'status']
    search_fields = ['user_name', 'contact']

    def get(self, request):
        if request.user.is_staff:
            queryset = UserTicket.objects.all()
        else:
            queryset = UserTicket.objects.filter(booking__user=request.user)

        serializer = UserTicketRetrieveSerializer(queryset, many=True)
        return CustomResponse.success(
            message="User tickets retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    @transaction.atomic
    def post(self, request):
        serializer = UserTicketCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse.success(
                message="User ticket created successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )


class UserTicketDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        ticket = UserTicket.objects.get(pk=pk)
        if not user.is_staff and ticket.booking.user != user:
            return None
        return ticket

    def get(self, request, pk):
        instance = self.get_object(pk, request.user)
        if not instance:
            return CustomResponse.error(
                message="User ticket not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = UserTicketRetrieveSerializer(instance)
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

        if instance.status == 'booked':
            return CustomResponse.error(
                message="Cannot modify a booked ticket",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserTicketUpdateSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse.success(
                message="User ticket updated successfully",
                data=serializer.data,
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
