import { USER, USERS, HOBBIES } from "./urls.ts";
import { RequestOptions } from "../types/index.ts";

function fetchFromCookie(name: string): string | null {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
}


async function logout() {
    const baseUrl = 'http://127.0.0.1:8000/';
    console.log(document.cookie)
    try {
        const csrfToken = fetchFromCookie('csrftoken');
        if (!csrfToken) {
            throw new Error('CSRF token not found');
        }
        console.log('CSRF Token:', csrfToken);
        const res = await fetch(baseUrl + "logout/", {
            method: "POST",
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken, // Use csrfToken directly after the null check
            }
        });
        console.log(res);
        if (res.ok) {
            window.location.href = baseUrl + "login/";
        } else {
            console.error("Logout unsuccessful");
        }
    } catch (error) {
        console.error(error);
        return false;
    }
}

async function sendRequest(url: string, options: RequestInit, params: URLSearchParams): Promise<any> {
    try {
        console.log(`Request Made To: ${url+params} with options: ${options}`)
        
        const response = await fetch(url + params, options);
        const data = await response.json();

        console.log(data);
        return data;
    } catch (error) {
        console.error(error);
    }
}

const createRequest = (method: string, baseUrl: string) => async ({ qParams = {}, body = null, id = null }: RequestOptions = {}): Promise<any> => {
    let token = fetchFromCookie('csrftoken');
    const url = `${baseUrl}${id ? `/${id}` : ''}`;
    const params = new URLSearchParams(qParams);

    // Ensure headers is typed correctly for TypeScript
    const headers: Record<string, string> = {
        'X-CSRFToken': token || '', // Provide an empty string if the token is not available
        'Content-Type': 'application/json',
    };

    const options: RequestInit = {
        method,
        credentials: 'include',
        headers,
        body: body ? JSON.stringify(body) : null,
    };

    const value = await sendRequest(url, options, params);
    return value;
};

async function registerNewHobby(data: {}): Promise<void> {
    let token = fetchFromCookie('csrftoken');
    console.log('HOBBY NAME: ' + name);
    
    const response = await fetch('http://127.0.0.1:8000/hobbies', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token || '',
        },
        credentials: 'include',
        body: JSON.stringify(data)
    })

    const newHobby = await response.json()
    console.log(newHobby)
  }


  async function sendFriendRequest(data: {}): Promise<void> {
    let token = fetchFromCookie('csrftoken');
    console.log(data)
    const response = await fetch('http://127.0.0.1:8000/send_friend_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token || '',
        },
        credentials: 'include',
        body: JSON.stringify(data)
    })

    const newRequest = await response.json()
    console.log(newRequest)
  }

  async function getAllPendingRequests(data: {}): Promise<void> {
    let token = fetchFromCookie('csrftoken');
    const response = await fetch('http://127.0.0.1:8000/get_friend_requests', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token || '',
        },
        credentials: 'include',
        body: JSON.stringify(data)
    })

    const newRequest = await response.json()
    return newRequest
  }

  async function updateUserProfile(id: string, data: Record<string, any>): Promise<any> {
    const csrfToken = fetchFromCookie('csrftoken');
    if (!csrfToken) {
        throw new Error('CSRF token not found');
    }

    const url = `http://127.0.0.1:8000/user/${id}/`;
    const options: RequestInit = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
        body: JSON.stringify(data),
    };

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error updating profile:', errorData);
            throw new Error('Failed to update profile');
        }
        return await response.json(); // Return the updated user data
    } catch (error) {
        console.error('Error in updateUserProfile:', error);
        throw error;
    }
}

async function getAllUsersByAge(startRange : number, endRange : number, hobbies : string[]): Promise<any> {
    const csrfToken = fetchFromCookie('csrftoken');
    if (!csrfToken) {
        throw new Error('CSRF token not found');
    }

    let data = {'startRange': startRange, 'endRange': endRange, 'hobbies': hobbies}

    const url = `http://127.0.0.1:8000/users_by_age`;
    const options: RequestInit = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
        body: JSON.stringify(data),
    };

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error fetching users by age:', errorData);
            throw new Error('Failed to fetch users by age');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in fetching users by age:', error);
        throw error;
    }
}

async function updatePasswordRequest(id: string, data: { currentPassword: string, newPassword: string }): Promise<any> {
    const csrfToken = fetchFromCookie('csrftoken');
    if (!csrfToken) {
        throw new Error('CSRF token not found');
    }

    const url = `http://127.0.0.1:8000/update-password/`;
    const options: RequestInit = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
        body: JSON.stringify(data),
    };

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error updating password:', errorData);
            throw new Error('Failed to update password');
        }
        return await response.json(); // Return a success message or any relevant data
    } catch (error) {
        console.error('Error in updatePassword:', error);
        throw error;
    }
}

async function acceptPendingRequest(id: number): Promise<any> {
    const csrfToken = fetchFromCookie('csrftoken');
    if (!csrfToken) {
        throw new Error('CSRF token not found');
    }

    const url = `http://127.0.0.1:8000/accept_friend_request/${id}/`;
    const options: RequestInit = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
    };

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error accepting friend request:', errorData);
            throw new Error('Failed to accept friend request');
        }
        return await response.json(); // Return a success message or any relevant data
    } catch (error) {
        console.error('Error in accepting friend request:', error);
        throw error;
    }
}
async function rejectPendingRequest(id: number): Promise<any> {
    const csrfToken = fetchFromCookie('csrftoken');
    if (!csrfToken) {
        throw new Error('CSRF token not found');
    }

    const url = `http://127.0.0.1:8000/reject_friend_request/${id}/`;
    const options: RequestInit = {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
    };

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error accepting friend request:', errorData);
            throw new Error('Failed to accept friend request');
        }
        return await response.json(); // Return a success message or any relevant data
    } catch (error) {
        console.error('Error in accepting friend request:', error);
        throw error;
    }
}


async function getAllFriends(): Promise<any> {
    const csrfToken = fetchFromCookie('csrftoken');
    if (!csrfToken) {
        throw new Error('CSRF token not found');
    }

    const url = `http://127.0.0.1:8000/get_all_friends`;
    const options: RequestInit = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
    };

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error getting friends:', errorData);
            throw new Error('Failed to fetch friends');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in fetching friends:', error);
        throw error;
    }
}




const getCurrentUserInfo = createRequest('GET', USER);
const getAllUsers = createRequest('GET', USERS);

const getProfile = createRequest('GET', USER);
const updateProfile = createRequest('PUT', USER);

const sortFriendsByAge = createRequest('GET', USERS);
const removeFriend = createRequest('DELETE', USERS)

const getAllHobbies = createRequest('GET', HOBBIES)
const addHobby = createRequest('PUT', HOBBIES)

const updatePassword = createRequest('PUT', `${USERS}/update-password`);

export { 
    getCurrentUserInfo, 
    getAllUsers, 
    getAllUsersByAge, 
    getProfile, 
    updateUserProfile, 
    getAllPendingRequests,
    sendFriendRequest, 
    rejectPendingRequest, 
    acceptPendingRequest, 
    getAllFriends, 
    sortFriendsByAge, 
    removeFriend,
    getAllHobbies, 
    addHobby, 
    logout, 
    fetchFromCookie,
    updatePassword,
    updatePasswordRequest,
    registerNewHobby
 };