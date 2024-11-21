from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from apps.events.serializers import (
    EventRetrieveSerializer,
    EventCreateSerializer,
    EventUpdateSerializer
)
from apps.events.models import Event
from apps.common.permissions import IsAdminOrReadOnly
from utils.response import CustomResponse


class EventListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def get(self, request):
        queryset = Event.objects.filter(date__gte=timezone.now().date()).order_by('-date')

        serializer = EventRetrieveSerializer(queryset, many=True)

        return CustomResponse.success(
            message="Events retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse.success(
                message="Event created successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return CustomResponse.error(
            message="Invalid event data",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class EventDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return None

    def get(self, request, pk):
        instance = self.get_object(pk)
        if not instance:
            return CustomResponse.error(
                message="Event not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = EventRetrieveSerializer(instance)
        return CustomResponse.success(
            message="Event details retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def put(self, request, pk):
        instance = self.get_object(pk)
        if not instance:
            return CustomResponse.error(
                message="Event not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = EventUpdateSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse.success(
                message="Event updated successfully",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        return CustomResponse.error(
            message="Invalid event data",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        instance = self.get_object(pk)
        if not instance:
            return CustomResponse.error(
                message="Event not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if instance.bookings.exists():
            return CustomResponse.error(
                message="Cannot delete event with existing bookings",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        instance.is_deleted = True
        instance.save()
        return CustomResponse.success(
            message="Event deleted successfully",
            status_code=status.HTTP_200_OK
        )
