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
      <div class="col-auto">
        <button class="btn btn-outline-primary" @click="sortByHobbies">Sort by Hobbies</button>
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
        <tr v-for="user in users" :key="user.id" >
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
import { getAllUsers, getAllUsersByAge, sendFriendRequest } from '../api/api';

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
      users: [] as any[],
      currentPage: 1,
      usersPerPage: 10,
      startRange: null,
      endRange: null
    };
  },
  computed: {
    start(): number {
      return (Number(this.currentPage) - 1) * Number(this.usersPerPage)
    },
    end(): number {
      return this.start + Number(this.usersPerPage)
    },
    totalPages(): number {
      return Math.ceil(this.users.length / this.usersPerPage);
    },
  },
  methods: {
    async paginatedUsers() {
      this.users = await getAllUsers({id: String(this.currentUser.id), body: {offset: this.start, limit: this.end }})
    },
    async filterByAge() {
      if (this.startRange !== null && this.endRange !== null) {
        this.users = await getAllUsersByAge({id: String(this.currentUser.id), body: { ageRangeStart: this.startRange, ageRangeEnd: this.endRange, offset: this.start, limit: this.end }});
      }
    },
    sortByHobbies() {
      for (const user of this.users) {
        let matchingSet = new Set([...this.currentUser.hobbies ?? []])
        user.matching = matchingSet.size 
      }
      this.users.sort((a, b) => a.matching - b.matching);
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
    changePage(page: number) {
      if (page > 0 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
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