"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponse

from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout_view, name='logout'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('users/', views.users, name='users'),
    path('users_by_age', views.get_users_by_age, name='users by age'),
    path('hobbies', views.hobbies, name='hobbies'),
    path('update-password/', views.update_password, name='update-password'),
    path('send_friend_request', views.send_friend_request_view, name='send friend request'),
    path('get_friend_requests', views.get_all_pending_requests, name='get all friend requests'),
    path('get_all_friends', views.get_all_friends, name='get all friends'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept friend request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject friend request'),
]
