import { defineStore } from 'pinia'
import { User } from '../types/index'
import { getCurrentUserInfo, fetchFromCookie } from '../api/api'

export const useGlobal = defineStore('global', {
    state: () => ({
        user: {
            id: 16,
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
            console.log("Saving user", this.user.id)
            if (this.user.id == null || this.user.id == undefined) {
                console.log("afasifnaosifnasoifn")
                this.user = await getCurrentUserInfo() as User;
            }
            console.log("ALL COOKIES: " + document.cookie)

            try {
                this.user = await getCurrentUserInfo() as User;
                console.log("CURRENT User:", this.user);
            } catch (error) {
                console.error("Error parsing user_data cookie:", error);
            }
            
        }
    }
})