<script setup>
import { ref } from "vue";
import axios from "axios";

const hits = ref(0);

try {
  const response = await axios.post("/hits");
  hits.value = parseInt(response.data.hits);
} catch (error) {
  console.error(error);
  hits.value = Math.floor(Math.random() * 10000);
}
</script>

<template>
  <main>
    <p>Welcome to the {{ hits }}nth visit of our app!!!</p>
  </main>
</template>
