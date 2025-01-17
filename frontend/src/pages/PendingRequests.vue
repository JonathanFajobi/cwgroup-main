<template>
  <div class="container">
    <h1 class="mb-3">Requests</h1>
    <table v-if="pendingRequests.length > 0" class="table table-hover">
    <thead>
      <tr>
        <th>User</th>
        <th>Status</th>
        <th>Accept</th>
        <th>Reject</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(request, userId) in pendingRequests" :key="userId">
        <td>{{ request.user_from.username }}</td>
        <td>{{ request.is_accepted ? 'Accepted' : 'Pending' }}</td>
        <td>
          <button class="btn btn-success" @click="acceptRequest(request.id)">
            Accept
          </button>
        </td>
        <td>
          <button class="btn btn-danger" @click="rejectRequest(request.id)">
            Reject
          </button>
        </td>
      </tr>
    </tbody>
  </table>

  </div>
</template>

<script lang="ts">
import { defineComponent, inject } from 'vue';
import { Request, User } from '../types';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import { getAllPendingRequests, acceptPendingRequest, rejectPendingRequest, fetchFromCookie } from '../api/api.ts';

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
      pendingRequests: {},
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
      const currentUser = JSON.parse(fetchFromCookie("user_data"))
      const currentUserHobbies = {'user_to_id': currentUser.id, 'user_to_name': currentUser.username};
      this.pendingRequests = await getAllPendingRequests(currentUserHobbies)
    },
    async acceptRequest(userToAcceptId: number) {
      toast("New friend added!", {
        autoClose: 1000
      });
      await acceptPendingRequest(userToAcceptId);
      this.paginatedRequests();
    },
    async rejectRequest(userToRejectId: number) {
      await rejectPendingRequest(userToRejectId);
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
    console.log(this.pendingRequests)
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
