from django.db import models

from apps.common.models import BaseModel


class Event(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    total_tickets = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
