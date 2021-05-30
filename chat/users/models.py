from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatRoom(models.Model):
    room_name = models.CharField(max_length=50)
    room_users = models.ManyToManyField(User)
    def __str__(self):
        return self.room_name