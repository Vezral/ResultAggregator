from django.contrib.auth.models import User
from django.db import models
from datetime import timezone


class Competition(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def get_creation_date(self):
        # convert to local timezone from default UTC
        creation_date = self.creation_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        return creation_date.strftime('X%d/X%m/%Y X%I:%M %p').replace('X0', 'X').replace('X', '')

    def get_start_time(self):
        # convert to local timezone from default UTC
        start_time = self.start_time.replace(tzinfo=timezone.utc).astimezone(tz=None)
        return start_time.strftime('X%d/X%m/%Y X%I:%M %p').replace('X0', 'X').replace('X', '')

    def __str__(self):
        if self.start_time is None:
            return '{} {}'.format(self.name, "No-Start-Time")
        else:
            return '{} {}'.format(self.name, self.get_start_time())

