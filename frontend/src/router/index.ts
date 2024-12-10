// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'
import { base } from '../api/urls';
// 1. Define route components.
// These can be imported from other files
import Home from '../pages/Home.vue';
import Friends from '../pages/friends.vue';
import Users from '../pages/users.vue';
import Profile from '../pages/profile.vue';
import PendingRequests from '../pages/PendingRequests.vue';


// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Home', component: Home },
        { path: '/friends/', name: 'Friends', component: Friends },
        { path: '/users/', name: 'Users', component: Users }, 
        { path: '/profile/', name: 'Profile', component: Profile },  
        { path: '/request/', name: 'Requests', component: PendingRequests }
        ]
    })

export default router
