from pickle import TRUE
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

statuschoices = (
    ("Normal", "Normal"),
    ("Premium", "Premium"),
    ("Admin", "Admin"),
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=100, default= "None", null=True)
    age = models.IntegerField(default=0, null=True)
    status = models.CharField(max_length=100, choices = statuschoices, default= "Normal")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


class Bookings(models.Model):
    date_time = models.DateTimeField(null=True)
    name = models.CharField(max_length=100, null=True)
    stats = models.CharField(max_length=100, null=True)
    

