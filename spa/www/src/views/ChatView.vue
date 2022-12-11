<script setup>
import { useWebSocket } from "@vueuse/core";
import { ref } from "vue";
import { useUser } from "../stores/user";
import { useCookies } from "@vueuse/integrations/useCookies";

const { token } = useUser();
const cookies = useCookies(["session"]);
console.log(token.value);
cookies.set("session", token.value);

const { data, send } = useWebSocket("ws://localhost/chat/ws");

const payload = ref("");

function sendMessage() {
  const ok = send(payload.value);
  if (ok) {
    payload.value = "";
  }
}
</script>

<template>
  <pre>Last Message: {{ data }}</pre>
  <input type="text" v-model="payload" />
  <button @click="sendMessage">Send</button>
</template>
