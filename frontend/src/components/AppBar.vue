<script setup>
import NavDrawer from "@/components/NavDrawer.vue";
import { useAuthStore } from "@/stores/useAuthStore";
import { ref } from "vue";
import { useTheme } from "vuetify";
import router from "@/router";

const theme = useTheme();
const darkTheme = ref(false);
const drawer = ref(false);

const authStore = useAuthStore();

function changeTheme() {
  darkTheme.value = !darkTheme.value;
  theme.global.name.value = darkTheme.value ? "dark" : "light";
  localStorage.setItem("darkTheme", darkTheme["value"]);
}

if (authStore.auth.isAuthenticated) {
  drawer.value = true;
}

const logOut = async() => {
  try {
    await authStore.logout();
    await router.push("/");
    window.location.reload();
  } catch (error) {
    console.error("Error during logout: ", error);
    throw error;
  }
}


const storedTheme = localStorage.getItem("darkTheme");
darkTheme.value = storedTheme === "true";
theme.global.name.value = darkTheme.value ? "dark" : "light";
</script>

<template>
  <v-app-bar
    border
    class="px-4"
    :elevation="0"
  >
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
    </template>

    <v-app-bar-title>
      <div v-if="authStore.auth.isAuthenticated">
        <RouterLink
          class="text-decoration-none text-h4 px-4 font-weight-light"
          :class="darkTheme ? 'text-white' : 'text-black'"
          to="/dashboard"
          >eBolnica
        </RouterLink>
      </div>
      <div v-else>
        <RouterLink
          class="text-decoration-none text-h4 px-4 font-weight-light"
          :class="darkTheme ? 'text-white' : 'text-black'"
          to="/"
          >eBolnica
        </RouterLink>
      </div>
    </v-app-bar-title>

    <v-spacer></v-spacer>

    <v-btn icon="true" @click="changeTheme" class="ml-6 mr-6">
      <v-icon
        :icon="darkTheme ? 'mdi-weather-sunny' : 'mdi-weather-night'"
      ></v-icon>
    </v-btn>
    <template v-slot:append>
      <RouterLink
          v-if="!authStore.auth.isAuthenticated"
          to="login">
        <v-btn
            variant="outlined"
            color="blue-darken-2"
            text="Prijavi se">
        </v-btn>
      </RouterLink>
      <v-btn
          append-icon="mdi-logout"
          @click="logOut"
          variant="flat"
          color="blue-darken-3"
          text="Odjavi se"
          v-else-if="authStore.auth.isAuthenticated">
      </v-btn>
    </template>
  </v-app-bar>
  <div>
    <NavDrawer v-model="drawer"></NavDrawer>
  </div>
</template>

<style scoped></style>
