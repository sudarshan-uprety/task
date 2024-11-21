from rest_framework import serializers

from apps.tickets.models import UserTicket
from apps.booking.models import Booking


class UserTicketSerializer(serializers.ModelSerializer):
    booking_id = serializers.PrimaryKeyRelatedField(
        queryset=Booking.objects.all(),
        source='booking'
    )

    class Meta:
        model = UserTicket
        fields = ['id', 'booking_id', 'status', 'user_name', 'contact']
        read_only_fields = ['status']

    def validate(self, data):
        # Ensure booking exists and has available tickets
        booking = data.get('booking')
        if not booking:
            raise serializers.ValidationError("Booking is required")

        # Additional validation logic can be added here
        return data