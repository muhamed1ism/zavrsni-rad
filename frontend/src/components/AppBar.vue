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

const logOut = async () => {
  try {
    await authStore.logout();
    await router.push("/");
    window.location.reload();
  } catch (error) {
    console.error("Error during logout: ", error);
    throw error;
  }
};

const storedTheme = localStorage.getItem("darkTheme");
darkTheme.value = storedTheme === "true";
theme.global.name.value = darkTheme.value ? "dark" : "light";
</script>

<template>
  <v-app-bar border class="px-4" :elevation="0">
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
    </template>

    <v-app-bar-title>
      <RouterLink
        class="text-decoration-none pl-2 font-weight-light"
        :class="darkTheme ? 'text-white' : 'text-black', $vuetify.display.smAndUp ? 'text-h4 pl-2' : 'text-h5'"
        :to="authStore.auth.isAuthenticated ? '/dashboard' : '/'"
        text="eBolnica"
      />
    </v-app-bar-title>


    <template v-slot:append>
      <v-btn
          icon
          @click="changeTheme"
          class="mr-3"
      >
        <v-icon
            :icon="darkTheme ? 'mdi-weather-sunny' : 'mdi-weather-night'"
        ></v-icon>
      </v-btn>
      <RouterLink v-if="!authStore.auth.isAuthenticated" to="/login" class="no-underline" >
        <v-btn v-if="$vuetify.display.smAndUp" append-icon="mdi-login" variant="outlined" color="blue-darken-2"
               text="Prijavi se" />
        <v-btn v-else slim size="small" icon="mdi-login" variant="outlined" color="blue-darken-2" rounded/>
      </RouterLink>

      <div v-else-if="authStore.auth.isAuthenticated">
        <v-btn v-if="$vuetify.display.smAndUp" slim append-icon="mdi-logout" @click="logOut" variant="flat"
            color="blue-darken-2" text="Odjavi se" />
        <v-btn v-else slim size="small" icon="mdi-logout" @click="logOut" variant="flat" color="blue-darken-2"
               rounded />
      </div>
    </template>
  </v-app-bar>

  <NavDrawer v-model="drawer"></NavDrawer>
</template>

<style scoped>
.no-underline {
  text-decoration: none;
}
</style>
