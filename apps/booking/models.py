from django.db import models

from apps.common.models import BaseModel
from apps.users.models import User
from apps.events.models import Event


class Booking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='bookings')
    status = models.BooleanField(default=True)
    booking_date = models.DateField()

    def __str__(self):
        return f'{self.user} {self.event} {self.booking_date}'
