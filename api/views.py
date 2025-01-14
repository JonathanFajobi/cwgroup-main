from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .models import User, Hobby, UserHobby
import json


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


''' View for logging in '''
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(username, password, user)
        if user is not None:
            print('Correct login details')
            auth_login(request, user)
        else:
            print('Invalid login details')

    return render(request, 'api/spa/login.html')


''' View for signing up '''
def signup(request):
    if request.method == 'POST':
        #Create new user
        user = User.objects.create_user(
            username = request.POST.get('username'),
            password = request.POST.get('password'),
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email'),
            date_of_birth = request.POST.get('dob')
        )

        selected_hobbies_ids = request.POST.get('habitats', [])
        if selected_hobbies_ids:
            selected_hobbies_ids = Hobby.objects.filter()
            user.hobbies.set(selected_hobbies_ids)

        print("Successfully created user")
        return JsonResponse(user.as_dict())
        
    return render(request, 'api/spa/signup.html')