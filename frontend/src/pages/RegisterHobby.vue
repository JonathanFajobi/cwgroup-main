<template>
    <div>
        <h1 class="mb-3">Register New Hobby</h1>
        <form @submit.prevent="submitNewHobby" method="POST">
            <div class="form-group">
                <label for="hobby-name">Hobby Name</label>
                <input type="text" class="form-control" id="hobby-name" name="hobby-name" v-model="hobbyFormData.hobbyName">
            </div>
            <div class="form-group">
                <button type="submit" class="btn btn-primary mx-2">Register New Hobby</button>
            </div>
        </form>
    </div>
</template>

<script lang="ts">
import { inject } from 'vue';
import { User } from '../types';
import { registerNewHobby} from '../api/api'

    export default {
    setup(){
        const globalState = inject('globalState') as { user: User }
        const currentUser = globalState.user
        return {
        currentUser
        }      
    },
    data() { 
        return {
            hobbyFormData: {
                hobbyName: ''
            }
        };
    },
    methods: {
        async submitNewHobby() {
            console.log("Registering new hobby", this.hobbyFormData.hobbyName);
            try {
                await registerNewHobby(this.hobbyFormData);
                console.log('Hobby added successfully');
            } catch (error) {
                console.error('Error adding hobby:', error);
            }
        }
    },
}
</script>