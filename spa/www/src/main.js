import { createApp } from "vue";
import { createPinia } from "pinia";
import { plugin, defaultConfig } from "@formkit/vue";
import "@formkit/themes/genesis";
import axios from "axios";

import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(plugin, defaultConfig);
app.use(createPinia());
app.use(router);

app.mount("#app");

// where we send back jwt stored in local storage
axios.interceptors.request.use(function (config) {
  config.headers["x-auth-token"] = localStorage.getItem("x-auth-token") || "";
  return config;
});
