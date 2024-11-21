from rest_framework import serializers
from django.utils import timezone

from apps.booking.models import Booking
from apps.users.serializers import UserDetailSerializer
from apps.events.models import Event
from apps.events.serializers import EventRetrieveSerializer


class BookingCreateSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = ['event', 'user', 'booking_date', 'status']
        read_only_fields = ['user', 'booking_date', 'status']
        extra_kwargs = {
            'event': {'required': True},
            'booking_date': {'required': True},
            'status': {'required': True}
        }

    def validate(self, data):
        event = data.get('event')
        if not event:
            raise serializers.ValidationError({"event": "Event is required"})

        booked_tickets = Booking.objects.filter(event=event, status=True).count()
        if booked_tickets >= event.total_tickets:
            raise serializers.ValidationError({"event": "No tickets available for this event"})

        data['booking_date'] = timezone.now().date()
        data['status'] = True

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['event'] = EventRetrieveSerializer(instance.event).data
        return representation


class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status']
        extra_kwargs = {
            'status': {'required': False}
        }

    def update(self, instance, validated_data):
        updated_instance = super().update(instance, validated_data)
        return BookingRetrieveSerializer(updated_instance).data


class BookingRetrieveSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    event = EventRetrieveSerializer()

    class Meta:
        model = Booking
        fields = ['id', 'event', 'user', 'status', 'booking_date']
