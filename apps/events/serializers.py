from rest_framework import serializers
from django.utils import timezone
from apps.events.models import Event


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'total_tickets']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'date': {'required': True},
            'location': {'required': True},
            'total_tickets': {'required': True}
        }

    def validate(self, data):
        if 'date' in data and data['date'] < timezone.now().date():
            raise serializers.ValidationError({"date": "Event date cannot be in the past"})

        if 'total_tickets' in data and data['total_tickets'] <= 0:
            raise serializers.ValidationError({"total_tickets": "Total tickets must be greater than 0"})

        return data


class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'total_tickets']
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'date': {'required': False},
            'location': {'required': False},
            'total_tickets': {'required': False}
        }

    def validate(self, data):
        if 'date' in data and data['date'] < timezone.now().date():
            raise serializers.ValidationError({"date": "Event date cannot be in the past"})

        if 'total_tickets' in data and data['total_tickets'] <= 0:
            raise serializers.ValidationError({"total_tickets": "Total tickets must be greater than 0"})

        return data

    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        return event


class EventRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'total_tickets']
