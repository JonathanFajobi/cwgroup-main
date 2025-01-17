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
            <input type="text" class="form-control" id="username" name="username" v-model="currentUser.username">
          </div>
          <div class="form-group">
            <label for="firstName">First Name</label>
            <input type="text" class="form-control" id="firstName" name="firstName" v-model="currentUser.firstName">
          </div>
          <div class="form-group">
            <label for="lastName">Last Name</label>
            <input type="text" class="form-control" id="lastName" name="lastName" v-model="currentUser.lastName">
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" name="email" v-model="currentUser.email">
          </div>
          <div class="form-group">
            <label for="dob">Date of Birth</label>
            <input type="date" class="form-control" id="dob" name="dob" v-model="currentUser.dob">
          </div>
          <div class="form-group">
            <label for="hobbies">Hobbies</label><br>
            <small class="form-text text-muted">Select Hobbies from the list below to add them to your profile</small>
            <select v-model="currentUser.hobbies" multiple class="form-control">
              <option v-for="(hobby) in availableHobbies.hobbies" :key="hobby.id" :value="hobby.id">
                {{ hobby.hobby_name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <router-link to="/register-hobby">Register a new hobby</router-link>
          </div>
          <div class="form-group">
            <label for="password">Current Password</label>
            <input type="password" class="form-control" id="currentPassword" name="currentPassword"
              v-model="currentPassword">
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
import { defineComponent, inject, computed } from 'vue';
import { User } from '../types';
import { getProfile, updateUserProfile, getAllHobbies, addHobby, updatePasswordRequest } from '../api/api';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default defineComponent({
  setup() {
    const globalState = inject('globalState') as { user: User; saveUser: () => void };
    const saveUserWrapper = () => {
      globalState.saveUser();
    };
    const currentUser = computed(() => globalState.user);

    return {
      currentUser,
      saveUserWrapper,
    };
  },
  created() {
    // Ensure user data is fetched on component creation
    console.log("Fetching user data...");
    this.saveUserWrapper();
  },
  data() {
    return {
      user: {} as User,
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
        // Populate the `user` object with data from `currentUser`, excluding hobbies.
        this.user = {
          username: this.currentUser.username,
          firstName: this.currentUser.firstName,
          lastName: this.currentUser.lastName,
          email: this.currentUser.email,
          dob: this.currentUser.dob
            ? new Date(this.currentUser.dob).toISOString().split('T')[0]
            : '',
          hobbies: new Set(), // Hobbies will not be pre-filled.
        };
      } catch (error) {
        console.error('Error loading profile:', error);
      }
    },
    async updateProfileWrapper() {
      try {
        const dateOfBirth = this.user.dob instanceof Date ? this.user.dob : new Date(this.user.dob);
        console.log("const dateOfBirth: " + dateOfBirth)
        console.log("const date_of_birth: " + dateOfBirth.toISOString().split('T')[0])

        const updatedUser = await updateUserProfile(String(this.currentUser.id), {
          username: this.currentUser.username,
          first_name: this.currentUser.firstName,
          last_name: this.currentUser.lastName,
          email: this.currentUser.email,
          date_of_birth: dateOfBirth ? dateOfBirth.toISOString().split('T')[0] : '',
          hobbies: Array.from(this.currentUser.hobbies || []), // Convert Set to Array if needed
        });
        console.log('Profile updated successfully:', updatedUser);
        this.currentUser = updatedUser; // Update the local state if necessary
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    },
    async getAllHobbiesWrapper() {
      this.availableHobbies = await getAllHobbies()
    },
    async addHobbyToDB() {
      if (this.hobbiesInput) {
        let result = await addHobby({ id: String(this.user.id), body: { hobby: this.hobbiesInput } })
        if (result) {
          this.hobbiesInput = '';
        } else {
          toast('An error occured, try again', {
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
        const success = await updatePasswordRequest(
          String(this.user.id),
          { currentPassword: this.currentPassword, newPassword: this.newPassword }
        );
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