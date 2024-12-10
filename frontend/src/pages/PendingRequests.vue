<template>
  <div class="container">
    <h1 class="mb-3">Requests</h1>
    <div class="row" v-for="request in pendingRequests" :key="request.id">
      <div class="col-8 align-self-center">
        <h5>{{ request.username }}</h5>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" @click="acceptRequest(request.id)" style="margin-right: '10px'">Accept</button>
      </div>
      <div class="col-auto">
        <button class="btn btn-outline-primary" @click="rejectRequest(request.id)">Reject</button>
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
import { Request, User } from '../types';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import { getAllPendingRequests, acceptPendingRequest, rejectPendingRequest } from '../api/api.ts';

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
      pendingRequests: [] as Request[],
      currentPage: 1,
      requestsPerPage: 10,
    };
  },
  computed: {
    start(): number {
      return (Number(this.currentPage) - 1) * Number(this.requestsPerPage)
    },
    end(): number {
      return this.start + Number(this.requestsPerPage)
    },
    totalPages(): number {
      return Math.ceil(this.pendingRequests.length / this.requestsPerPage);
    },
  },
  methods: {
    async paginatedRequests() {
      this.pendingRequests = await getAllPendingRequests({id: String(this.currentUser.id), body: {offset: this.start, limit: this.end }})
    },
    async acceptRequest(userToAcceptId: number) {
      toast("New friend added!", {
        autoClose: 1000
      });
      await acceptPendingRequest({ id: String(this.currentUser.id), body: userToAcceptId });
      this.paginatedRequests();
    },
    async rejectRequest(userToRejectId: number) {
      await rejectPendingRequest({ id: String(this.currentUser.id), body: userToRejectId });
      this.paginatedRequests()
    },
    changePage(page: number) {
      if (page > 0 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
  },
  mounted() {
    this.paginatedRequests();
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
