from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


def login(request):
    return render(request, 'api/spa/login.html')

def signup(request):
    return render(request, 'api/spa/signup.html')