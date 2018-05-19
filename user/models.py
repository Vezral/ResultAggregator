from django.db import models
from django.contrib.auth.models import User
from competition.models import Competition
from django.db.models.signals import post_save
from django.dispatch import receiver


# contains additional info for User registered in student group
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    competition = models.ManyToManyField(Competition)

    def __str__(self):
        return '{} {}'.format(self.user.username, self.competition.all())


# whenever user in student group is updated, update its student model as well
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.groups.filter(name='Student').exists():
        instance.student.save()
