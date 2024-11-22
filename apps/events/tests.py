from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.events.models import Event
from apps.booking.models import Booking
from apps.users.models import User


class EventTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            full_name='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.normal_user = User.objects.create_user(
            full_name='user',
            email='user@test.com',
            password='testpass123'
        )

        # Create test event
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date() + timezone.timedelta(days=10),
            location='Test Location',
            total_tickets=100
        )

        self.client = APIClient()

    def test_list_events_authenticated(self):
        """Test retrieving events list as authenticated user"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_create_event_as_admin(self):
        """Test creating event as admin user"""
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            'title': 'New Event',
            'description': 'New Description',
            'date': (timezone.now().date() + timezone.timedelta(days=5)).isoformat(),
            'location': 'New Location',
            'total_tickets': 50
        }
        response = self.client.post(reverse('event-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)

    def test_create_event_as_normal_user(self):
        """Test creating event as normal user it must fails"""
        self.client.force_authenticate(user=self.normal_user)
        payload = {
            'title': 'New Event',
            'description': 'New Description',
            'date': (timezone.now().date() + timezone.timedelta(days=5)).isoformat(),
            'location': 'New Location',
            'total_tickets': 50
        }
        response = self.client.post(reverse('event-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_event_with_bookings(self):
        """Test deleting event that has bookings it must fail"""
        self.client.force_authenticate(user=self.admin_user)

        # Create a booking for the event
        Booking.objects.create(
            user=self.normal_user,
            event=self.event,
            booking_date=timezone.now().date()
        )

        response = self.client.delete(reverse('event-detail', args=[self.event.id]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
