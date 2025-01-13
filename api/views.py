from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User


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
        print("attempting to sign up")
    return render(request, 'api/spa/signup.html')