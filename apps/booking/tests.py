from unittest.mock import patch

import pytest

from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.events.models import Event
from apps.booking.models import Booking
from apps.tickets.models import UserTicket
from apps.users.models import User


class BookingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            full_name='sudarshan uprety',
            email='sudarshan.uprety@khalti.com',
            password='ifyouknowyouknow'
        )

        self.event = Event.objects.create(
            title='Shakti pradrshan by UML Nepal.',
            description='Event in Kathmandu by UML party of Nepal',
            date=timezone.now().date() + timezone.timedelta(days=10),
            location='Kathmandu valley',
            total_tickets=2
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_booking(self):
        """Test creating a new booking"""
        payload = {
            'event': self.event.id,
            'booking_date': timezone.now().date().isoformat()
        }
        response = self.client.post(reverse('booking-list'), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_cancel_booking_within_24_hours(self):
        """Test canceling a booking within 24 hours of event (should fail)"""
        event = Event.objects.create(
            title='CHitwan Rhinos vs Sudhur Pachim',
            description='NPL match',
            date=timezone.now().date() + timezone.timedelta(days=1),
            location='TU Ground.',
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
        """Test handling concurrent bookings for last ticket 1 must fail and another should work"""

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

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.count(), 1)


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            full_name='suds uprety',
            email='no-reply@sudarshan-uprety.com.np',
            password='itmustpass123'
        )

        self.event = Event.objects.create(
            title='Khalti NPL',
            description='NPL event in Kathmandu',
            date=timezone.now().date() + timezone.timedelta(days=10),
            location='Khalti Office',
            total_tickets=100
        )

    def test_event_str_representation(self):
        """Test the string representation of Event model"""
        self.assertEqual(str(self.event), 'Khalti NPL')

    def test_booking_str_representation(self):
        """Test the string representation of Booking model"""
        booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            booking_date=timezone.now().date()
        )
        expected_str = f'{self.user} {self.event} {booking.booking_date}'
        self.assertEqual(str(booking), expected_str)

    def test_user_ticket_str_representation(self):
        """Test the string representation of UserTicket model"""
        booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            booking_date=timezone.now().date()
        )
        ticket = UserTicket.objects.create(
            booking=booking,
            user_name='Test User',
            contact='1234567890'
        )
        expected_str = ticket.user_name + ticket.booking.event.title
        self.assertEqual(str(ticket), expected_str)
