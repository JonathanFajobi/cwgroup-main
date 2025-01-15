const BASE_ = 'http://127.0.0.1:8000';
let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''
// For JSON server testing
// BASE_DOMAIN = 'http://localhost:3000';
const BASE_URL = BASE_ + '/api';
const USER = BASE_URL + '/user'
const USERS = BASE_URL + '/users'
const HOBBIES = BASE_URL + '/hobbies'

export { USER, USERS, HOBBIES, base }