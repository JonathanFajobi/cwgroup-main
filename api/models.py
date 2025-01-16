from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

#Create your models here

class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"


class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField('Hobby', related_name='users', blank=True)
    matching_users = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='matched_by')

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
    
    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'dob': self.date_of_birth,
            'hobbies': [hobby.id for hobby in self.hobbies.all()],
            'matching': [self.matching_users.id for self in self.matching_users.all()]
        }


class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'hobby_name': self.name
        }

class UserHobby(models.Model):
    ''' Through class for link between User and Hobby '''

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    hobby = models.ForeignKey('Hobby', on_delete=models.CASCADE)

    def as_dict(self):
        return {
            'id': self.id,
            'user': self.user,
            'hobby': self.hobby
        }  


class FriendRequest(models.Model):
    user_from = models.ForeignKey(User, related_name='requests_sent', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='requests_received', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_from.username} -> {self.user_to.username}"
