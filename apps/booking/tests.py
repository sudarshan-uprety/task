from unittest.mock import patch

import pytest

from django.urls import reverse
from django.utils import timezone
from django.db import transaction

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.events.models import Event
from apps.booking.models import Booking
from apps.users.models import User


class BookingTests(APITestCase):
    def setUp(self):
        print('1')
        self.user = User.objects.create_user(
            full_name='testuser',
            email='test@test.com',
            password='testpass123'
        )

        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date() + timezone.timedelta(days=10),
            location='Test Location',
            total_tickets=2
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_booking(self):
        print('2')
        """Test creating a new booking"""
        payload = {
            'event': self.event.id,
            'booking_date': timezone.now().date().isoformat()
        }
        response = self.client.post(reverse('booking-list'), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_cancel_booking_within_24_hours(self):
        print('3')
        """Test canceling a booking within 24 hours of event (should fail)"""
        event = Event.objects.create(
            title='Tomorrow Event',
            description='Test Description',
            date=timezone.now().date() + timezone.timedelta(days=1),
            location='Test Location',
            total_tickets=1
        )

        booking = Booking.objects.create(
            user=self.user,
            event=event,
            booking_date=timezone.now().date()
        )

        response = self.client.delete(reverse('booking-detail', args=[booking.id]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db(transaction=True)
    def test_concurrent_booking(self):
        print('4')
        """Test handling concurrent bookings for last ticket"""

        def create_booking():
            with transaction.atomic():
                return self.client.post(reverse('booking-list'), {
                    'event': self.event.id,
                    'booking_date': timezone.now().date().isoformat()
                })

        # Simulate two concurrent bookings
        with patch('django.db.transaction.on_commit', lambda f: f()):
            response1 = create_booking()
            response2 = create_booking()
            print('response 1', response1)
            print('response 2', response2)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.count(), 1)
