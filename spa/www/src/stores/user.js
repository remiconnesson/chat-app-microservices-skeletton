import { ref, computed } from "vue";

const _token = ref(localStorage.getItem("x-auth-token") || "");

export const useUser = () => {
  const isLoggedIn = computed(() => _token.value !== "");

  function setToken(token) {
    _token.value = token || "";
    localStorage.setItem("x-auth-token", token);
  }

  function logOut() {
    setToken("");
  }

  return { token: _token, isLoggedIn, setToken, logOut };
};
