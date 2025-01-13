from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
    
class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dateOfBirth = models.DateField()
    hobbies = models.ManyToManyField('Hobby', related_name='users', blank=True)
    
    def __str__(self):
        return self.username
    
class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
class FriendRequest(models.Model):
    userFrom = models.ForeignKey(User, related_name='requestsSent', on_delete=models.CASCADE)
    userTo = models.ForeignKey(User, related_name='requestsReceived', on_delete=models.CASCADE)
    isAccepted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.userFrom.username} -> {self.userTo.username}"