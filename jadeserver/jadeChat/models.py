from django.db import models

class Chat(models.Model):
    id = models.CharField(max_length=10)
    user1 = models.CharField(max_length=100)
    user2 = models.CharField(max_length=100)
    messages = models.CharField(max_length=999999999)
    name = models.CharField(max_length=1000, default="My Chat")
