from django.db import models
from django.contrib.auth.models import AbstractUser

#Create your models here

class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"


class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    hobbies = models.ManyToManyField('Hobby', related_name='users', blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  #Reverse accessor clash fix
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  #Reverse accessor clash fix
        blank=True
    )

    def __str__(self):
        return self.username


class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class FriendRequest(models.Model):
    user_from = models.ForeignKey(User, related_name='requests_sent', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='requests_received', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_from.username} -> {self.user_to.username}"
