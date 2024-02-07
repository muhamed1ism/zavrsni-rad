<script setup>
import {useUserStore} from "@/stores/useUserStore";
import {useAuthStore} from "@/stores/useAuthStore";
import {usePatientStore} from "@/stores/usePatientStore";
import {useDoctorStore} from "@/stores/useDoctorStore";
import {ref} from "vue";

const authStore = useAuthStore();
const userStore = useUserStore();
const role = userStore.user.role;
const profile = role === "patient" ? usePatientStore().patient : useDoctorStore().doctor;
profile.email = userStore.user.email;

const navItems = [
  {
    title: "O nama",
    icon: "mdi-information",
    to: "/about",
  },
  {
    title: "Kontaktirajte nas",
    icon: "mdi-phone",
    to: "/contact",
  },
];

if (!authStore.auth.isAuthenticated) {
  navItems.splice(0, 0, {
    title: "Početna stranica",
    icon: "mdi-home",
    to: "/",
  });
  navItems.splice(1, 0, {
    title: "Prijavi se",
    icon: "mdi-login",
    to: "/login",
  });
} else {
  navItems.splice(0, 0, {
    title: "Početna stranica",
    icon: "mdi-view-dashboard",
    to: "/dashboard",
  });
}

if (role === "patient") {
  navItems.splice(1, 0, {
    title: "Moj profil",
    icon: "mdi-account",
    to: "/patient",
  });
  navItems.splice(2, 0, {
    title: "Moji termini",
    icon: "mdi-calendar-clock",
    to: "/appointments",
  });
  navItems.splice(3, 0, {
    title: "Zakaži pregled",
    icon: "mdi-calendar-plus",
    to: "/appointments/create",
  });
  navItems.splice(4, 0, {
    title: "Doktori",
    icon: "mdi-account-group",
    to: "/doctors",
  });
  navItems.splice(5, 0, {
    title: "Postavke",
    icon: "mdi-cog",
    to: "/settings",
  });
} else if (role === "doctor") {
  navItems.splice(1, 0, {
    title: "Moj profil",
    icon: "mdi-account",
    to: "/doctor",
  });
  navItems.splice(2, 0, {
    title: "Termini",
    icon: "mdi-calendar-clock",
    to: "/appointments",
  });
  navItems.splice(3, 0, {
    title: "Upravljanje terminima",
    icon: "mdi-calendar-edit",
    to: "/appointments/manage",
  })
  navItems.splice(4, 0, {
    title: "Pacijenti",
    icon: "mdi-account-group",
    to: "/patients",
  });
  navItems.splice(5, 0, {
    title: "Doktori",
    icon: "mdi-account-group",
    to: "/doctors",
  });
  navItems.splice(6, 0, {
    title: "Postavke",
    icon: "mdi-cog",
    to: "/settings",
  });
}
</script>

<template>
  <v-navigation-drawer width="300" location="left" permanent>
    <v-list color="blue-darken-2" nav>
      <v-list-item
          v-if="authStore.auth.isAuthenticated"
          lines="two"
          prepend-icon="mdi-account-circle"
          :title="profile.firstName + ' ' + profile.lastName"
          :subtitle="profile.email"
      ></v-list-item>
      <v-list-item
          v-for="item in navItems"
          :key="item.title"
          :prepend-icon="item.icon"
          :link="true"
          :to="item.to"
          :title="item.title"
      ></v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<style scoped>

</style>