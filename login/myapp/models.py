from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# class CustomUser(AbstractUser):
#     # Add any additional fields here
#     surname = models.CharField(max_length=100, null=True, blank=True)
#     name = models.CharField(max_length=100, null=True, blank=True)
# models.py

class Channel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class ChannelMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'channel')

    def __str__(self):
        return f"{self.user.username} in {self.channel.name}"