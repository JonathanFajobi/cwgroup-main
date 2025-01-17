from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from api.models import User, Hobby, UserHobby
from django.shortcuts import redirect
import json
from urllib.parse import quote
from datetime import date


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
            
            # Create a response to redirect to the frontend
            response = redirect('http://127.0.0.1:5173/')

            # Prepare the user's data to store in the cookie
            user_data = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'dob': user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else None,
                'hobbies': [hobby.name for hobby in user.hobbies.all()],
                'matching_users': [matched_user.id for matched_user in user.matching_users.all()]
            }

            # Serialize the user data as JSON
            serialized_user_data = json.dumps(user_data)
            encoded_user_data = quote(serialized_user_data)

            # Set a new cookie with the user data
            response.set_cookie('user_data', encoded_user_data, max_age=3600, secure=False, samesite='Lax')
            return response
        else:
            print('Invalid login details')
            

    return render(request, 'api/spa/login.html')


def logout_view(request):
    if request.method == "POST":
        logout(request)
        print("logout successful")
        response = JsonResponse({"message": "Logged out successfully"}, status=200)
        return response
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

def user(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'GET':
        print(request.user.is_authenticated, request.user)
        if request.user.is_authenticated:
            if request.user.id == user_id:
                return JsonResponse(user.as_dict())
            else:
                return HttpResponseForbidden("You are not authorized to view this data.")    
        return HttpResponseForbidden("You need to log in to view this data.")
    
    if request.method == 'PUT':
        if request.user.is_authenticated and request.user.id == user_id:
            try:
                data = json.loads(request.body)
                
                # Safely handle hobbies
                if 'hobbies' in data and data['hobbies'] is not None:
                    if isinstance(data['hobbies'], list):  # Validate it's a list
                        user.hobbies.set(data['hobbies'])
                    else:
                        return HttpResponseBadRequest("Hobbies must be a list of IDs.")
                
                if 'username' in data: user.username = data.get('username', user.username)
                if 'first_name' in data: user.first_name = data.get('first_name', user.first_name)
                if 'last_name' in data: user.last_name = data.get('last_name', user.last_name)
                if 'email' in data: user.email = data.get('email', user.email)
                if 'date_of_birth' in data: user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
                user.save()
                return JsonResponse({"message": "Profile updated successfully."})
            except json.JSONDecodeError:
                return HttpResponseBadRequest("Invalid JSON format.")
        return HttpResponseForbidden("You are not authorized to update this data.")
    
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_data = [user.as_dict() for user in users]
        for user in users_data:
            user['age'] = calculate_age(user)
        
        username_of_requester = request.user
        thisUser = find_user_by_name(username_of_requester)
        sort_users_by_hobbies(thisUser['hobbies'], users_data)
        return JsonResponse(users_data, safe=False)

def calculate_age(self):
    if self['dob']:
        today = date.today()
        age = today.year - self['dob'].year
        if (today.month, today.day) < (self['dob'].month, self['dob'].day):
            age -= 1
        return age
    return None

def get_users_by_age(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        startRange = data.get('startRange')
        endRange = data.get('endRange')
        hobbies = data.get('hobbies')
        users = User.objects.all()
        users_data = [user.as_dict() for user in users]

        for user in users_data:
            user['age'] = calculate_age(user)

        sorted_users = sort_users_by_value(users_data, 'age', startRange, endRange)
        sort_users_by_hobbies(hobbies, sorted_users)
        return JsonResponse(sorted_users, safe=False)
    return JsonResponse({})

def sort_users_by_value(users, value, startRange, endRange):
    sorted_users = sorted(users, key=lambda x: (x[value] is None, x[value]))

    filtered_users = [
        user for user in sorted_users 
        if user[value] is not None and startRange <= user[value] <= endRange
    ]
    
    return filtered_users

def sort_users_by_hobbies(hobbies, users):
    target_hobbies = set(hobbies)  # Convert target_hobbies to a set
    users_with_common_hobbies = []

    for user in users:
        user_hobbies = set(user.get('hobbies', []))  # Convert user_hobbies to a set
        print(user_hobbies, target_hobbies)
        common_hobbies_count = len(user_hobbies & target_hobbies)  # Set intersection
        user['common_hobbies'] = common_hobbies_count
        users_with_common_hobbies.append(user)

    users_with_common_hobbies.sort(key=lambda x: x['common_hobbies'], reverse=True)
    
    for user in users_with_common_hobbies:
        user.pop('common_hobbies', None)

    return users_with_common_hobbies


def find_user_by_name(username):
    users = User.objects.all()
    users_data = [user.as_dict() for user in users]
    for user in users_data:
        if str(user['username']) == str(username):
            return user





''' API for list of hobbies'''
def hobbies(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            print(data)
            hobby_name = data.get('hobbyName')  # Retrieve the hobby_name
            if not hobby_name:  # Handle missing or empty hobby_name
                return JsonResponse({"error": "Hobby name is required"}, status=400)
            
            hobby = Hobby.objects.create(name=hobby_name)
            return JsonResponse(hobby.as_dict())
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    
    return JsonResponse({
        'hobbies': [hobby.as_dict() for hobby in Hobby.objects.all()]
    })
