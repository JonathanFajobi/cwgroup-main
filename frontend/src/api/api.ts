import { USER, USERS, HOBBIES, base } from "./urls.ts";
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
            window.location.href = baseUrl;
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
    const params = new URLSearchParams(qParams)

    const options: RequestInit = {
        method,
        credentials: "include",
        headers: {
            'X-CSRFToken': token,
            'Content-Type': 'application/json'
        },
        body: body ? JSON.stringify(body) : null
    };
    const value = await sendRequest(url, options, params);
    return value;
};

const getCurrentUserInfo = createRequest('GET', USER);
const getAllUsers = createRequest('GET', USERS);
const getAllUsersByAge = createRequest('GET', USERS);
const getAllUsersByMatchingHobbies = createRequest('GET', USERS);

const getProfile = createRequest('GET', USERS);
const updateProfile = createRequest('PUT', USERS);

const getAllPendingRequests = createRequest('GET', USERS);
const rejectPendingRequest = createRequest('DELETE', USERS);
const acceptPendingRequest = createRequest('POST', USERS);
const sendFriendRequest = createRequest('POST', USERS)

const getAllFriends = createRequest('GET', USERS);
const sortFriendsByAge = createRequest('GET', USERS);
const removeFriend = createRequest('DELETE', USERS)

const getAllHobbies = createRequest('GET', HOBBIES)
const addHobby = createRequest('POST', HOBBIES)

const updatePassword = createRequest('PUT', `${USERS}/update-password`);

export { 
    getCurrentUserInfo, 
    getAllUsers, 
    getAllUsersByAge, 
    getAllUsersByMatchingHobbies, 
    getProfile, 
    updateProfile, 
    getAllPendingRequests, 
    rejectPendingRequest, 
    acceptPendingRequest, 
    getAllFriends, 
    sortFriendsByAge, 
    sendFriendRequest, 
    removeFriend,
    getAllHobbies, 
    addHobby, 
    logout, 
    fetchFromCookie,
    updatePassword
 };