<script setup>
import { RouterLink, RouterView } from "vue-router";
import { useUser } from "./stores/user";

const { token, isLoggedIn, logOut } = useUser();
</script>

<template>
  {{ isLoggedIn }}
  {{ token }}
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <div v-if="isLoggedIn">
          <button @click="logOut">Logout</button>
          <RouterLink to="/chat">Chat</RouterLink>
        </div>
        <RouterLink v-else to="/register">Register</RouterLink>
      </nav>
    </div>
  </header>

  <!--- https://vuejs.org/guide/built-ins/suspense.html#combining-with-other-components --> 
  <RouterView v-slot="{ Component }">
    <template v-if="Component">
      <Suspense>
        <!-- main content -->
        <component :is="Component"></component>

        <!-- loading state -->
        <template #fallback> Loading... </template>
      </Suspense>
    </template>
  </RouterView>
</template>
