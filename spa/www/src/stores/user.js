import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useUserStore = defineStore("user", () => {
  const _token = ref("");

  const isLoggedIn = computed(() => _token.value !== "");

  function setToken(token) {
    _token.value = token || "";
    localStorage.setItem('x-auth-token', token);
  }

  function logOut() {
    setToken("");
  }

  return { isLoggedIn, setToken, logOut };
});
