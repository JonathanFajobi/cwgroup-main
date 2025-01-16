<template>
    <nav class="navbar navbar-expand-lg navbar-primary fixed-top shadow">
        <div class="container-fluid">
            <div class="navbar-nav">
                <router-link class="nav-link text-light" :to="{name: 'Home'}">Home <i class="bi bi-house-fill"></i></router-link>
                <router-link class="nav-link text-light" :to="{name: 'Friends'}">Friends <i class="bi bi-heart-fill"></i></router-link>
                <router-link class="nav-link text-light" :to="{name: 'Users'}" >Users <i class="bi bi-people"></i></router-link>
                <router-link class="nav-link text-light" :to="{name: 'Requests'}" >Requests <i class="bi bi-inbox-fill"></i></router-link>
                <router-link class="nav-link text-light" :to="{name: 'Profile'}" >Profile</router-link>
                <component v-if="currentUser.id">
                    <router-link class="nav-link text-light" @click="logoutWrapper" :to="{name: ''}">Logout</router-link>
                </component>
            </div>
        </div>
    </nav>
    <main class="container pt-5 mt-5">
        <RouterView class="flex-shrink-0 rounded p-4 lightergray text-secondary" />
    </main>
</template>

<script lang="ts">
import { defineComponent, onMounted, provide } from "vue";
import { logout } from "./api/api";
import { RouterView } from "vue-router";
import { useGlobal } from "./stores/global";

export default defineComponent({
    setup() {
        const globalState = useGlobal()
        provide('globalState', globalState)

        return {
            currentUser: globalState.user
        }
    },
    methods: {
        async logoutWrapper() {
            await logout()
        }
    },
    components: { RouterView },
});

</script>

<style>
@import 'bootstrap-icons/font/bootstrap-icons.css';
@import '../src/styles/styles.css';

.navbar-primary {
    background-color: #007bff;
}
.shadow {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
