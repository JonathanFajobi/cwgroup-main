<template>
  <h1 class="h1">
    Hello, {{ currentUser.username }}
  </h1>
  <h6 class="text-muted mb-5">Welcome to your feed, click on the buttons to navigate to a new page!</h6>
  <router-link to="/friends/">
    <button class="btn btn-outline-primary rounded mb-3 shadow home-button">
      <h2>Friends</h2>
    </button>
  </router-link>
  <router-link to="/profile/">
    <button class="btn btn-outline-primary rounded mb-3 shadow home-button">
      <h2>Profile</h2>
    </button>
  </router-link>
  <router-link to="/request/">
    <button class="btn btn-outline-primary rounded mb-3 shadow home-button">
      <h2>Requests</h2>
    </button>
  </router-link>
</template>

<script lang="ts">
import { defineComponent, inject, computed } from "vue";
import { User } from "../types";
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
});
</script>

<style scoped>
.home-button {
  width: 80vw;
}
</style>
