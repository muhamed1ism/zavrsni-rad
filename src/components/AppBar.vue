<script setup>
import { onMounted, ref } from "vue";
import { useTheme } from "vuetify";
import NavDrawer from "@/components/NavDrawer.vue";
import {useAuthStore} from "@/stores/useAuthStore";

const theme = useTheme();
const darkTheme = ref(false);
const drawer = ref(false);

const authStore = useAuthStore()

function changeTheme() {
  darkTheme.value = !darkTheme.value;
  theme.global.name.value = darkTheme.value ? "dark" : "light";
  localStorage.setItem("darkTheme", darkTheme["value"]);
}

async function logOut() {
  try {
    await authStore.logout();
  } catch (error) {
    console.log('Error during logout: ', error);
  }
}

onMounted(() => {
  const storedTheme = localStorage.getItem("darkTheme");
  darkTheme.value = storedTheme === "true";
  theme.global.name.value = darkTheme.value ? "dark" : "light";
});
</script>

<template>
  <v-app-bar
    border
    class="px-4"
    :elevation="0"
    scroll-behavior="collapse elevate"
  >
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
    </template>

    <v-app-bar-title>
      <div v-if="authStore.isAuthenticated">
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
      <v-btn
          to="/login"
          variant="outlined"
          color="blue-darken-2"
          text="Prijavi se"
          v-if="!authStore.isAuthenticated"
      >
      </v-btn>

      <v-btn
          @click="logOut"
          variant="flat"
          color="blue-darken-2"
          text="Odjavi se"
          v-else-if="authStore.isAuthenticated"
      >
        Odjavi se
        <v-icon class="pl-4">mdi-logout</v-icon>
      </v-btn>
    </template>
  </v-app-bar>
    <div>
      <NavDrawer v-model="drawer"></NavDrawer>
    </div>
</template>

<style scoped></style>
