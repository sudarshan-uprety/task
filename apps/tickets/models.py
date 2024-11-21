from django.db import models

from apps.common.models import BaseModel
from apps.booking.models import Booking


class UserTicket(BaseModel):
    ACTION_TYPES = (
        ('available', 'Available'),
        ('booked', 'Booked')
    )
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=10, choices=ACTION_TYPES, default='available'
    )
    user_name = models.CharField(max_length=120, null=False, blank=False)
    contact = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.user_name + self.booking.event.title
