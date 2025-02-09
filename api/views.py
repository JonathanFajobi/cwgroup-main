from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from api.models import User, Hobby, FriendRequest
from django.shortcuts import redirect
import json
from urllib.parse import quote
from datetime import date, datetime
from django.db.models import Q


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

''' FRIEND REQUESTS VIEWS '''

def send_friend_request_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)

        user_from_name = data.get('senderName')
        user_to_name = data.get('recipientName')
        user_from_id = data.get('senderId')
        user_to_id = data.get('recipientId')

        request_string = f"{user_from_name} -> {user_to_name}"
        request_string_alt = f"{user_to_name} -> {user_from_name}"
        print("Sender:", user_from_name)
        print("Recipient:", user_to_name)

        all_friend_requests = FriendRequest.objects.all()
        all_friend_requests_data = [str(friend_request) for friend_request in all_friend_requests]

        if check_if_friend_request_exists(request_string, all_friend_requests_data):
            return HttpResponse("Friend request already exists.", status=400)
        if check_if_friend_request_exists(request_string_alt, all_friend_requests_data):
            return HttpResponse("Friend request already exists.", status=400)

        user_from = User.objects.filter(id=user_from_id).first()
        user_to = User.objects.filter(id=user_to_id).first()

        if not user_from or not user_to:
            return HttpResponse("Invalid user IDs", status=400)

        friend_request = FriendRequest.objects.create(
            user_from=user_from,
            user_to=user_to,
            is_accepted=False
        )

        return JsonResponse({'id': friend_request.id, 'user_from': user_from.username, 'user_to': user_to.username, 'is_accepted': friend_request.is_accepted})
    
def get_all_pending_requests(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_to_id = data.get('user_to_id')

        user_to = User.objects.get(id=user_to_id)

        pending_requests = FriendRequest.objects.filter(user_to=user_to, is_accepted=False)

        friend_requests_data = [request.as_dict() for request in pending_requests]
        return JsonResponse(friend_requests_data, safe=False)
    

def get_all_friends(request):
    if request.method == "GET":
        user_id = request.user.id
        all_friends = FriendRequest.objects.filter(
            Q(user_from=user_id) | Q(user_to=user_id),
            is_accepted=True)

        friends = []

        for friend_request in all_friends:
            if friend_request.user_from.id == user_id:
                friends.append(friend_request.user_to.as_dict())
            elif friend_request.user_to.id == user_id:
                friends.append(friend_request.user_from.as_dict())

        return JsonResponse(friends, safe=False)


def accept_friend_request(request, request_id):
    if request.method == 'PUT':
        friend_request = FriendRequest.objects.get(id=request_id)

        if friend_request.is_accepted:
            return JsonResponse({'message': 'Friend request already accepted'}, status=400)

        friend_request.is_accepted = True

        friend_request.save()

        return JsonResponse(friend_request.as_dict(), status=200)
    
def reject_friend_request(request, request_id):
    if request.method == 'DELETE':
        friend_request = FriendRequest.objects.get(id=request_id)

        if friend_request.is_accepted:
            return JsonResponse({'message': 'Friend request already accepted, cannot reject it'}, status=400)

        friend_request.delete()

        return JsonResponse({'message': 'Friend request rejected and deleted successfully'}, status=200)


def check_if_friend_request_exists(new_friend_request, all_requests):
    for request in all_requests:
        print(request)
        if str(request) == str(new_friend_request):
            return True
    return False


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
            selected_hobbies = Hobby.objects.filter(id__in=selected_hobbies_ids)
            user.hobbies.set(selected_hobbies)
            user.save()
            
        response = redirect('http://127.0.0.1:8000/login/')

        print("Successfully created user")
        return response
        
    hobbies = Hobby.objects.all()  # Get all hobbies
    return render(request, 'api/spa/signup.html', {'hobbies': hobbies})

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
                        # Fetch hobbies by name
                        hobbies_objects = Hobby.objects.filter(name__in=data['hobbies'])
                        # If any hobby name doesn't exist, return an error
                        if len(hobbies_objects) != len(data['hobbies']):
                            return HttpResponseBadRequest("One or more hobby names are invalid.")
                        
                        # Overwrite the user's hobbies with the new list of Hobby objects
                        user.hobbies.set(hobbies_objects)
                    else:
                        return HttpResponseBadRequest("Hobbies must be a list of names.")
                    
                if 'date_of_birth' in data:
                    if data['date_of_birth']:  # Only update if a valid date is provided
                        try:
                            user.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                        except ValueError:
                            return HttpResponseBadRequest("Invalid date format. Please use YYYY-MM-DD.")
                    else:
                        # Retain the current date_of_birth if not provided or invalid
                        user.date_of_birth = user.date_of_birth
                
                if 'username' in data: user.username = data.get('username', user.username)
                if 'first_name' in data: user.first_name = data.get('first_name', user.first_name)
                if 'last_name' in data: user.last_name = data.get('last_name', user.last_name)
                if 'email' in data: user.email = data.get('email', user.email)
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
        sorted_users = sort_users_by_hobbies(thisUser['hobbies'], users_data, request.user)
        return JsonResponse(sorted_users, safe=False)

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
        sorted_users = sort_users_by_hobbies(hobbies, sorted_users, request.user)
        return JsonResponse(sorted_users, safe=False)
    return JsonResponse({})

def sort_users_by_value(users, value, startRange, endRange):
    sorted_users = sorted(users, key=lambda x: (x[value] is None, x[value]))

    filtered_users = [
        user for user in sorted_users 
        if user[value] is not None and startRange <= user[value] <= endRange
    ]
    
    return filtered_users

def sort_users_by_hobbies(hobbies, users, this_user):
    target_hobbies = set(hobbies)  # Convert target_hobbies to a set
    users_with_common_hobbies = []

    for user in users:
        user_hobbies = set(user.get('hobbies', []))  # Convert user_hobbies to a set
        common_hobbies_count = len(user_hobbies & target_hobbies)  # Set intersection
        user['common_hobbies'] = common_hobbies_count
        users_with_common_hobbies.append(user)

    users_with_common_hobbies.sort(key=lambda x: x['common_hobbies'], reverse=True)
    
    for user in users_with_common_hobbies:
        user.pop('common_hobbies', None)

    print(users_with_common_hobbies)
    index = 0
    for user in users_with_common_hobbies:
        if user['id'] == this_user.id:
            print("made it here")
            users_with_common_hobbies.pop(index)
        index+=1

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

def update_password(request):
    if request.method == 'PUT':
        # Get the current user (assumed that user is authenticated)
        user = request.user
        
        # Retrieve the current password and new password from the request body
        data = json.loads(request.body)
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')

        # Check if the current password matches
        if not check_password(current_password, user.password):
            return JsonResponse({'error': 'Current password is incorrect'}, status=400)

        # Update the password
        user.set_password(new_password)
        user.save()

        # Update the session to avoid logout
        update_session_auth_hash(request, user)

        return JsonResponse({'message': 'Password successfully updated'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)