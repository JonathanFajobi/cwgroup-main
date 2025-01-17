<template>
  <div class="container">
    <h1 class="mb-3">Users</h1>

    <div class="row mb-3">
      <div class="col-auto">
        <div class="input-group">
          <button class="btn btn-outline-primary" @click="filterByAge">Sort by Age</button>
          <input type="number" v-model="startRange" placeholder="Start Age" class="form-control" />
          <input type="number" v-model="endRange" placeholder="End Age" class="form-control" />
        </div>
        </div>
    </div>
    <div class="card" style="overflow:hidden; border-radius: 10px; margin-bottom: 1rem; border: none;">
    <table class="table table-hover">
      <thead>
        <tr>
          <th>Name</th>
          <th>Age</th>
          <th>Hobbies</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in paginatedUsers" :key="user.id">
          <td>{{ user.username }}</td>
          <td>{{ user.age }}</td>
          <td>{{ Array.from(user.hobbies).join(', ') }}</td>
          <td>
            <button class="btn btn-primary" @click="sendRequest(user.id, user.username)">Send Request</button>
          </td>
        </tr>
      </tbody>
    </table>
    </div>
    <nav>
      <ul class="pagination">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">Previous</a>
        </li>
        <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
          <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">Next</a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script lang="ts">
import { defineComponent, inject } from 'vue';
import { User } from '../types';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import { getAllUsers, getAllUsersByAge, sendFriendRequest, getCurrentUserInfo, fetchFromCookie } from '../api/api';

export default defineComponent({
  setup() {
    const globalState = inject('globalState') as { user: User }
    const currentUser = globalState.user
    return {
      currentUser
    }
  },
  data() {
    return {
      users: [],  // Full list of users
      currentPage: 1,  // Current page number
      usersPerPage: 4,  // Users to display per page
      startPageRange: 0,
      endPageRange: 4,
      startRange: null,  // Starting index for users on the current page
      endRange: null  // Ending index for users on the current page
    };
  },
  computed: {
    paginatedUsers() {
      this.startPageRange = (this.currentPage - 1) * this.usersPerPage;
      this.endPageRange = this.startPageRange + this.usersPerPage;
      return this.users.slice(this.startPageRange, this.endPageRange);
    },
    totalPages() {
      return Math.ceil(this.users.length / this.usersPerPage);  // Total number of pages
    }
  },
  methods: {
    async paginatedUsers() {
      this.users = await getAllUsers({id: String(this.currentUser.id), body: {offset: this.start, limit: this.end }})
    },
    async filterByAge() {
      if (this.startRange !== null && this.endRange !== null) {
        const currentUser = JSON.parse(fetchFromCookie("user_data"))
        const currentUserHobbies = currentUser.hobbies;
        this.users = await getAllUsersByAge(this.startRange, this.endRange, currentUserHobbies);
      }
    },
    async sortByHobbies() {
      console.log(fetchFromCookie("user_data"))
      const currentUser = JSON.parse(fetchFromCookie("user_data"))
      const currentUserHobbies = Object.assign({}, currentUser.hobbies);
      console.log(currentUserHobbies)
    },
    sendRequest(userId: number, username: string) {
      sendFriendRequest({id: String(userId), body: this.currentUser}).then(() => {
        toast("Request sent!", {
          autoClose: 1000
        })
      }).then(() => {
        console.log(`Request sent to ${username} with ID: ${userId}`);
      }).catch((err) => console.error(err))
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    }
  },
  async mounted() {
    this.users = await getAllUsers()
  },
});
</script>

<style scoped>
.lightergray {
    color:rgb(234, 234, 234)
}

.container {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
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