<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/register">Register</RouterLink>
      </nav>
    </div>
  </header>

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
