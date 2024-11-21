from django.utils import timezone

from rest_framework import serializers

from apps.booking.models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['event', 'user', 'booking_date', 'status']
        read_only_fields = ['user', 'booking_date', 'status']
        extra_kwargs = {
            'events': {'required': True},
            'booking_date': {'required': True},
            'status': {'required': True}
        }

    def validate(self, data):
        # Check if event exists
        event = data.get('event')
        if not event:
            raise serializers.ValidationError("Event is required")

        # Check if event has available tickets
        booked_tickets = Booking.objects.filter(event=event).count()
        print(booked_tickets)
        if booked_tickets >= event.total_tickets:
            raise serializers.ValidationError("No tickets available for this event")

        # Set booking date to current date
        data['booking_date'] = timezone.now().date()

        # Set default status to True
        data['status'] = True

        return data

    def create(self, validated_data):
        # Get the current user from context
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class BookingRetrieveSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_date = serializers.DateField(source='event.date', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'event', 'event_title', 'event_date', 'user', 'status', 'booking_date']


class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status']

    def validate(self, data):
        # Additional validation if needed
        return data
