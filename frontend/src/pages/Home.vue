<template>
  <h1 class="h1">
    Hello, {{ currentUser.username }}
  </h1>
  <h6 class="text-muted mb-5">Welcome to your feed, click on the buttons to navigate to a new page!</h6>
  <a href="/friends/">
    <button class="btn btn-outline-primary rounded mb-3 shadow home-button"><h2>Friends</h2></button>
  </a>
  <a href="/profile/">
    <button class="btn btn-outline-primary rounded mb-3 shadow home-button"><h2>Profile</h2></button>
  </a>
  <a href="/request/">
    <button class="btn btn-outline-primary rounded mb-3 shadow home-button" ><h2>Requests</h2></button>
  </a>
</template>

<script lang="ts">
    import { defineComponent, inject } from "vue";
    import { User } from "../types"; 
    export default defineComponent({
        setup() {
          const globalState = inject('globalState') as { user: User, saveUser: () => void }
          const saveUserWrapper = () => { globalState.saveUser()  } 
          const currentUser = globalState.user
            return {
            currentUser,
            saveUserWrapper
          }        
        }, 
        mounted() {
          console.log(this.currentUser)
          this.saveUserWrapper()
        }
    })
</script>

<style scoped>
.home-button {
    width: 80vw;
}
</style>
