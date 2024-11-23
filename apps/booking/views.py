from django.utils import timezone
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404

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
from utils.email import send_booking_confirmation
from utils.pdf import BookingPDF


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
        serializer = BookingCreateSerializer(queryset, many=True)
        return CustomResponse.success(
            message="Bookings retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            booking = serializer.save()
            send_booking_confirmation(booking=booking)
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


class BookingPDFDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        booking = get_object_or_404(Booking, id=pk, user=self.request.user)
        return booking

    def get(self, request, pk):
        booking = self.get_object(pk)
        pdf = BookingPDF()
        pdf.add_page()

        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f'Booking Reference: #{booking.id}', ln=True)
        pdf.ln(10)

        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Event Details', ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Event: {booking.event}', ln=True)
        pdf.cell(0, 10, f'Date: {booking.booking_date}', ln=True)
        pdf.cell(0, 10, f'Status: {"Active" if booking.status else "Inactive"}', ln=True)
        pdf.ln(10)

        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'User Information', ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Name: {booking.user.full_name}', ln=True)
        pdf.cell(0, 10, f'Email: {booking.user.email}', ln=True)

        pdf_content = pdf.output(dest='S').encode('latin1')

        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="booking_{booking.id}.pdf"'

        return response