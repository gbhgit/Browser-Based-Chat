from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=50)
    room_users = models.ManyToManyField(User)
    
    def __str__(self):
        return self.room_name

class Post(models.Model):
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
    msn = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.msn