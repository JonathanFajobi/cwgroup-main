from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


''' View for logging in '''
def login(request):
    if request.method == 'POST':
        post_username = request.POST.get('username')
        post_password = request.POST.get('password')

        user = authenticate(username=post_username, password=post_password)
        if user is not None:
            auth_login(request, user)
        else:
            print('Invalid login details')

    return render(request, 'api/spa/login.html')


''' View for signing up '''
def signup(request):
    if request.method == 'POST':
        print("attempting to sign up")
    return render(request, 'api/spa/signup.html')