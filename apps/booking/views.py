from django.utils import timezone
from django.test import TestCase

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from apps.booking.models import Booking
from apps.booking.serializers import (
    BookingCreateSerializer,
    BookingRetrieveSerializer,
    BookingUpdateSerializer
)
from utils.response import CustomResponse


class BookingListView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event', 'user', 'status']
    search_fields = ['event__title']

    def get(self, request):
        if request.user.is_staff:
            queryset = Booking.objects.all().select_related('event', 'user').order_by('-booking_date')
        else:
            queryset = Booking.objects.filter(
                user=request.user
            ).select_related(
                'event', 'user'
            ).order_by('-booking_date')
        serializer = BookingRetrieveSerializer(queryset, many=True)
        return CustomResponse.success(
            message="Bookings retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse.success(
                message="Booking created successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )


class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            if not self.request.user.is_staff and booking.user != self.request.user:
                return None
            return booking
        except Booking.DoesNotExist:
            return None

    def get(self, request, pk):
        instance = self.get_object(pk)
        if not instance:
            return CustomResponse.error(
                message="Booking not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = BookingRetrieveSerializer(instance)
        return CustomResponse.success(
            message="Booking details retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def put(self, request, pk):
        instance = self.get_object(pk)
        if not instance:
            return CustomResponse.error(
                message="Booking not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if instance.event.date <= timezone.now().date() + timezone.timedelta(days=1):
            return CustomResponse.error(
                message="Cannot modify booking within 24 hours of event",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer = BookingUpdateSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            return CustomResponse.success(
                message="Booking updated successfully",
                data=data,
                status_code=status.HTTP_200_OK
            )

    def delete(self, request, pk):
        instance = self.get_object(pk)
        if not instance:
            return CustomResponse.error(
                message="Booking not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if instance.event.date <= timezone.now().date() + timezone.timedelta(days=1):
            return CustomResponse.error(
                message="Cannot cancel booking within 24 hours of event",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        instance.is_deleted = True
        instance.save()
        return CustomResponse.success(
            message="Booking cancelled successfully",
            status_code=status.HTTP_200_OK
        )
