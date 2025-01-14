from django.contrib import admin

# Register your models here.

from .models import User, Hobby, UserHobby

admin.site.register(User)
admin.site.register(Hobby)
admin.site.register(UserHobby)