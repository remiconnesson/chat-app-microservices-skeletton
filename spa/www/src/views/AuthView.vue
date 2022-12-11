<script setup>
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/user";
import axios from "axios";

const router = useRouter();
const { setToken } = useUserStore();

const registering = ref(true);
const register = () => (registering.value = true);
const signin = () => (registering.value = false);

const error = ref("");

const submitted = ref(false);
const submitHandler = async (credentials) => {
  const endpoint = registering.value ? "/auth/register" : "/auth/login";
  console.log(credentials);
  try {
    const response = await axios.post(endpoint, credentials);
    submitted.value = true;
    setToken(response.headers["x-auth-token"]);
    router.push("/");
  } catch (e) {
    console.error(e);
    error.value = e.response.data.error;
    submitted.value = false;
  }
};

// prepopulate somefields to accelerate dev
function makeAccount(username, email, password) {
  const account = { username, email, password };
  if (!registering.value) delete account.username;
  return account;
}

const accounts = ref([]);

const selectedAccountIndex = ref(0);

const formContent = ref();

watch(
  [selectedAccountIndex, registering],
  ([index]) => {
    accounts.value = [
      makeAccount("", "", ""),
      makeAccount("remiremi", "remiremi@gmail.com", "12345678"),
      makeAccount("remi2", "remiremi2@gmail.com", "AZERT123"),
    ];
    formContent.value = accounts.value[index];
  },
  { immediate: true }
);
</script>

<template>
  <button v-if="!registering" @click="register">Register</button>
  <button v-else @click="signin">Sign In</button>
  <br />
  <select v-model="selectedAccountIndex">
    <option v-for="(_, index) in accounts" :key="index">{{ index }}</option>
  </select>
  <pre v-if="error" style="color: red">ERROR {{ error }}</pre>
  <FormKit
    type="form"
    id="registration"
    :form-class="submitted ? 'hide' : 'show'"
    :submit-label="registering ? 'Register' : 'Signin'"
    @submit="submitHandler"
    :actions="false"
    v-model="formContent"
  >
    <h1 v-if="registering">Register!</h1>
    <h1 v-else>Sign In!</h1>
    <p></p>
    <hr />
    <FormKit
      v-if="registering"
      type="text"
      name="username"
      label="Your username"
      placeholder="Jane Doe"
      help="What do people call you?"
      validation="required"
    />
    <FormKit
      type="text"
      name="email"
      label="Your email"
      placeholder="jane@example.com"
      help="What email should we use?"
      validation="required|email"
    />
    <FormKit
      type="password"
      name="password"
      label="Password"
      validation="required|length:5|matches:/[^a-zA-Z]/"
      :validation-messages="{
        matches: 'Please include at least one symbol',
      }"
      placeholder="Your password"
      help="Choose a password"
    />

    <FormKit
      type="submit"
      :submit-label="registering ? 'Register' : 'Signin'"
    />
  </FormKit>
  <div v-if="submitted">
    <h2>Submission successful!</h2>
  </div>
</template>
