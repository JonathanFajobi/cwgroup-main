<template>
  <div class="container">
    <h1 class="mb-3">Profile</h1>
    <div class="row">
    <div class="col-6">
      <div class="card-body">
        <div>
          <p class="mb-5"><strong>Username:</strong> {{ currentUser.username }}</p>
          <p class="mb-5"><strong>First Name:</strong> {{ currentUser.first_name }}</p>
          <p class="mb-5"><strong>Last Name:</strong> {{ currentUser.last_name }}</p>
          <p class="mb-5"><strong>Email:</strong> {{ currentUser.email }}</p>
          <p class="mb-5"><strong>Date of Birth:</strong> {{ currentUser.dob }}</p>
          <p class="mb-5"><strong>Hobbies:</strong> {{ Array.from(currentUser.hobbies).join(', ') }}</p>
        </div>
      </div>
    </div>
    <div class="col-6">
    <form @submit.prevent="updateProfileWrapper">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" class="form-control" id="username" name="username" v-model="user.username">
      </div>
      <div class="form-group">
        <label for="firstName">First Name</label>
        <input type="text" class="form-control" id="firstName" name="firstName" v-model="user.firstName">
      </div>
      <div class="form-group">
        <label for="lastName">Last Name</label>
        <input type="text" class="form-control" id="lastName" name="lastName" v-model="user.lastName">
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" class="form-control" id="email" name="email" v-model="user.email">
      </div>
      <div class="form-group">
        <label for="dob">Date of Birth</label>
        <input type="date" class="form-control" id="dob" name="dob" v-model="user.dob">
      </div>
      <div class="form-group">
        <label for="hobbies">Hobbies</label>
        <input type="text" class="form-control" id="hobbies" name="hobbies" v-model="hobbiesInput" @keydown.enter="addHobbyToDB">
        <small class="form-text text-muted">Press Enter to add a hobby</small>
        <select v-model="user.hobbies" multiple class="form-control">
          <option v-for="(hobby) in availableHobbies.hobbies" :key="hobby.id" :value="hobby.hobby_name">
            {{ hobby.hobby_name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="password">Current Password</label>
        <input type="password" class="form-control" id="currentPassword" name="currentPassword" v-model="currentPassword">
      </div>
      <div class="form-group">
        <label for="newPassword">New Password</label>
        <input type="password" class="form-control" id="newPassword" name="newPassword" v-model="newPassword">
      </div>
      <button type="button" class="btn btn-secondary" @click="updatePassword">Update Password</button>
      <button type="submit" class="btn btn-primary mx-2">Update Profile</button>
    </form>
  </div>
</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, inject } from 'vue';
import { User } from '../types';
import { getProfile, updateProfile, getAllHobbies, addHobby, updatePassword } from '../api/api';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default defineComponent({
  setup(){
    const globalState = inject('globalState') as { user: User }
    const currentUser = globalState.user
      return {
      currentUser
    }      
  },
  data() {
    return {
      user:{} as User,
      hobbiesInput: '',
      editingPassword: false,
      currentPassword: '',
      newPassword: '',
      availableHobbies: new Set(),
    };
  },
  methods: {
    async loadProfile() {
      try {
        const profile = await getProfile({ id: String(this.user.id) });
        this.user = {
          ...profile,
          hobbies: new Set(profile.hobbies)
        };
      } catch (error) {
        console.error('Error loading profile:', error);
      }
    },
    async updateProfileWrapper() {
      try {
        await updateProfile({ 
          id: String(this.user.id), 
          body: { ...this.user, hobbies: Array.from(this.user.hobbies)  
          } 
        });
        console.log('Profile updated successfully');
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    },
    async getAllHobbiesWrapper() {
      this.availableHobbies = await getAllHobbies()
    }, 
    async addHobbyToDB() {
      if (this.hobbiesInput) {
        let result = await addHobby({id: String(this.user.id), body: {hobby: this.hobbiesInput} })
        if (result) {
          this.hobbiesInput = '';
        } else {
          toast('An error occured, try again',{
            type: 'warning',
            autoClose: 2000
          })
        }
      }
    },
    editPassword() {
      this.editingPassword = true;
    },
    async updatePassword() {
      try {
        const success = await updatePassword({
          id: String(this.user.id),
          body: { currentPassword: this.currentPassword, newPassword: this.newPassword }
        });
        if (success) {
          toast("Password successfully updated!", {
            type: 'success',
            autoClose: 1000
          });
          this.currentPassword = '';
          this.newPassword = '';
        } else {
          toast("An error occurred, try again!", {
            type: 'warning',
            autoClose: 1000
          });
        }
      } catch (error) {
        console.error('Error updating password:', error);
      }
    },
  },
  mounted() {
    this.loadProfile();
    this.getAllHobbiesWrapper()
  },
});
</script>

<style scoped>
.container {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
}
.form-group {
  margin-bottom: 15px;
}
.row {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 10px;
  background-color: #f8f9fa;
}
.btn {
  border-radius: 5px;
}
.pagination {
  justify-content: center;
}
.page-item.disabled .page-link {
  pointer-events: none;
  cursor: default;
}
.page-item.active .page-link {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
}
</style>