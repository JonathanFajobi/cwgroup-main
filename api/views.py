from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


def cars_api(request):
    return JsonResponse({
        'cars': [
            {
                'make': 'Toyota',
                'model': 'Corolla',
                'year': 2010,
                'color': 'red',
            },
            {
                'make': 'Toyota',
                'model': 'Camry',
                'year': 2015,
                'color': 'blue',
            },
            {
                'make': 'Honda',
                'model': 'Civic',
                'year': 2012,
                'color': 'black',
            },
        ]
    })
