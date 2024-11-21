from rest_framework import serializers

from apps.tickets.models import UserTicket
from apps.booking.models import Booking


class UserTicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTicket
        fields = ['booking', 'status', 'user_name', 'contact']
        read_only_fields = ['status']
        extra_kwargs = {
            'booking': {'required': True},
            'user_name': {'required': True},
            'contact': {'required': True}
        }

    def validate(self, data):
        booking = data.get('booking')
        if not booking:
            raise serializers.ValidationError({"booking": "Booking is required"})

        # Check if ticket already exists
        if UserTicket.objects.filter(booking=booking, status='booked').exists():
            raise serializers.ValidationError({"booking": "Ticket already exists for this booking"})

        return data


class UserTicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTicket
        fields = ['status', 'user_name', 'contact']
        extra_kwargs = {
            'status': {'required': False},
            'user_name': {'required': False},
            'contact': {'required': False}
        }


class UserTicketRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTicket
        fields = ['id', 'booking', 'status', 'user_name', 'contact']