from django.db import models


class Competition(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        if self.start_time is None:
            return '{} {}'.format(self.name, "No-Start-Time")
        else:
            return '{} {}'.format(self.name, self.start_time)

