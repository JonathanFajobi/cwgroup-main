from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from api.models import User, Hobby, UserHobby
from django.shortcuts import redirect

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
            return redirect('http://localhost:5173/')
        else:
            print('Invalid login details')

    return render(request, 'api/spa/login.html')


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logged out successfully"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)


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

        selected_hobbies_ids = request.POST.getlist('hobbies')
        if selected_hobbies_ids:
            selected_hobbies = Hobby.objects.filter(name__in=selected_hobbies_ids)
            user.hobbies.set(selected_hobbies)
            user.save()

        print("Successfully created user")
        return JsonResponse(user.as_dict())
        
    return render(request, 'api/spa/signup.html')

def user(request):
    if request.method == 'GET':
        toReturn = request.user.as_dict()
        return JsonResponse(toReturn)

def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_data = [user.as_dict() for user in users]
        return JsonResponse(users_data, safe=False)

def hobbies(request):
    if request.method == 'POST':
        hobby = Hobby.objects.create(
            name = request.POST.get('name')
        )
        return JsonResponse(hobby.as_dict())

    return JsonResponse({
        'hobbies': [hobby.as_dict() for hobby in Hobby.objects.all()]
    })