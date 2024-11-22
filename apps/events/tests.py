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
            full_name='Sudarshan Uprety',
            email='no-reply@sudarshan-uprety.com.np',
            password='itwillpass123'
        )
        self.normal_user = User.objects.create_user(
            full_name='Suds Uprety',
            email='admin@sudarshan-uprety.com.np',
            password='thismustnotpass123'
        )

        self.event = Event.objects.create(
            title='Australia Event Test',
            description='Students test',
            date=timezone.now().date() + timezone.timedelta(days=10),
            location='Putalisadak',
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
            'title': 'Sungava College Fest',
            'description': 'Welcome and farewell by Sungava College.',
            'date': (timezone.now().date() + timezone.timedelta(days=5)).isoformat(),
            'location': 'Hotel Seven Star, Sauraha Chitwan',
            'total_tickets': 300
        }
        response = self.client.post(reverse('event-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)

    def test_create_event_as_normal_user(self):
        """Test creating event as normal user it must fails"""
        self.client.force_authenticate(user=self.normal_user)
        payload = {
            'title': 'Sungava College Fest',
            'description': 'Welcome and farewell by Sungava College.',
            'date': (timezone.now().date() + timezone.timedelta(days=5)).isoformat(),
            'location': 'Hotel Seven Star, Sauraha Chitwan',
            'total_tickets': 300
        }
        response = self.client.post(reverse('event-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_event_with_bookings(self):
        """Test deleting event that has bookings it must fail"""
        self.client.force_authenticate(user=self.admin_user)

        Booking.objects.create(
            user=self.normal_user,
            event=self.event,
            booking_date=timezone.now().date()
        )

        response = self.client.delete(reverse('event-detail', args=[self.event.id]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
