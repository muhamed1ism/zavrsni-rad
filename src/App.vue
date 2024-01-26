<template>
  <v-app>
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
        <RouterLink
          class="text-decoration-none text-h4 px-4 font-weight-light"
          :class="darkTheme ? 'text-white' : 'text-black'"
          to="/"
          >eBolnica
        </RouterLink>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <v-btn icon @click="changeTheme" class="ml-6 mr-6">
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
        >
        </v-btn>
      </template>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" location="left" temporary>
      <v-list-item title="My Application" subtitle="Vuetify"></v-list-item>
      <v-divider></v-divider>
      <v-list-item link title="List Item 1"></v-list-item>
      <v-list-item link title="List Item 2"></v-list-item>
      <v-list-item link title="List Item 3"></v-list-item>
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>

    <v-footer app dense absolute border>
      <div class="px-4 py-2 text-center w-100">
        {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
      </div>
    </v-footer>
  </v-app>
</template>

<script setup>
import { onMounted } from "vue";
import { ref } from "vue";
import { useTheme } from "vuetify";

const theme = useTheme();
const darkTheme = ref(false);
const drawer = ref(false);

function changeTheme() {
  darkTheme.value = !darkTheme.value;
  theme.global.name.value = darkTheme.value ? "dark" : "light";
  localStorage.setItem("darkTheme", darkTheme.value);
}

onMounted(() => {
  const storedTheme = localStorage.getItem("darkTheme");
  darkTheme.value = storedTheme === "true";
  theme.global.name.value = darkTheme.value ? "dark" : "light";
});
</script>
