<template>
  <div class="container">
    <h1 class="mb-3">Friends</h1>
    <div class="row" v-for="friend in friends" :key="friend.id">
      <div class="col-10">
        <h5>{{ friend.username }}</h5>
        <p>Main hobbies: {{ Array.from(friend.hobbies).join(', ') }}</p>
      </div>
      <div class="col-2 align-self-center">
        <button class="btn btn-primary" @click="removeFriendWrapper(friend.id)">Remove Request</button>
      </div>
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
import { Friend, User } from '../types';
import { getAllFriends, sortFriendsByAge, removeFriend } from '../api/api';

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
      friends: [] as Friend[],
      currentPage: 1,
      friendsPerPage: 10,
    };
  },
  computed: {
    start(): number {
      return (Number(this.currentPage) - 1) * Number(this.friendsPerPage)
    },
    end(): number {
      return this.start + Number(this.friendsPerPage)
    },
    totalPages(): number {
      return Math.ceil(this.friends.length / this.friendsPerPage);
    },
  },
  methods: {
    async paginatedFriends() {
      this.friends = await getAllFriends()
    },
    async removeFriendWrapper(id: number) {
      removeFriend({id: String(id) })
    }, 
    changePage(page: number) {
      if (page > 0 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
  },
  mounted() {
    this.paginatedFriends();
  },
});
</script>

<style scoped>
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
