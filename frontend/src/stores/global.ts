import { defineStore } from 'pinia'
import { User } from '../types/index'
import { getCurrentUserInfo, fetchFromCookie } from '../api/api'

export const useGlobal = defineStore('global', {
    state: () => ({
        user: {
            id: 1, 
            username: "Placeholder Username", 
            firstName: "Placeholder First Name", 
            lastName: "Placeholder Last Name",
            email: "Placeholder@gmail.com",
            dob: new Date(),
            hobbies: new Set(['hobby1', 'hobby2']),
            matching: null
        } as User, 
    }),  
    actions: {
        async saveUser() {
            console.log("Saving user")
            if (this.user.id == null || this.user.id == undefined) {
                const id = parseInt(fetchFromCookie("user_id"));
                this.user = await getCurrentUserInfo({ id: String(id) }) as User;
            }
        }
    }
})