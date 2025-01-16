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
                const id = parseInt(fetchFromCookie("user_data") || "0");
                this.user = await getCurrentUserInfo({ id: String(id) }) as User;
            }
            console.log("ALL COOKIES: " + document.cookie)
            console.log("User Cookie: " + fetchFromCookie("user_data"))

            const userData = fetchFromCookie("user_data");
            if (userData) {
                try {
                    const parsedData = JSON.parse(userData); // Parse the JSON string
                    const id = parsedData.id ? parseInt(parsedData.id, 10) : 0; // Extract and parse the ID
                    console.log("User ID:", id);
                    this.user = await getCurrentUserInfo({ id: String(id) }) as User;
                    console.log("CURRENT User:", this.user);
                } catch (error) {
                    console.error("Error parsing user_data cookie:", error);
                }
            } else {
                console.log("No user_data cookie found.");
            }
        }
    }
})