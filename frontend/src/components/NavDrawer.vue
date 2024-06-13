<script setup>
import { useUserStore } from "@/stores/useUserStore";
import { useAuthStore } from "@/stores/useAuthStore";
import { usePatientStore } from "@/stores/usePatientStore";
import { useDoctorStore } from "@/stores/useDoctorStore";
import router from "@/router";
import ProfilePicture from "@/components/ProfilePicture.vue";

const authStore = useAuthStore();
const userStore = useUserStore();
const patientStore = usePatientStore();
const doctorStore = useDoctorStore();

const profile = (userStore.user.role === "patient") ? patientStore.patient : doctorStore.doctor;

const navItems = [
  ...authStore.auth.isAuthenticated
    ? [
        {
          title: "Nadzorna ploča",
          icon: "mdi-view-dashboard",
          to: "/dashboard",
        },
        {
          title: "Moj profil",
          icon: "mdi-card-account-details",
          to: "/profile",
        },
      ]
    : [{ title: "Početna stranica", icon: "mdi-home", to: "/" }],

  ...userStore.user.role === "patient"
    ? [
        {
          title: "Moji termini",
          icon: "mdi-calendar-clock",
          to: "/appointments",
        },
        {
          title: "Zakaži pregled",
          icon: "mdi-calendar-plus",
          to: "/appointments/create",
        },
        { title: "Doktori", icon: "mdi-account-group", to: "/doctors" },
        {
          title: "Upravljanje računom",
          icon: "mdi-account-wrench",
          to: "/account-management",
        },
      ]
    : [],

  ...userStore.user.role === "doctor"
    ? [
        {
          title: "Svi naručeni termini",
          icon: "mdi-calendar-clock",
          to: "/appointments",
        },
        {
          title: "Upravljanje terminima",
          icon: "mdi-calendar-edit",
          to: "/appointments/manage",
        },
        {
          title: "Moji pacijenti",
          icon: "mdi-account-multiple",
          to: "/patients",
        },
        { title: "Svi doktori", icon: "mdi-account-group", to: "/doctors" },
        {
          title: "Upravljanje računom",
          icon: "mdi-account-wrench",
          to: "/account-management",
        },
      ]
    : [],

  { title: "O nama", icon: "mdi-information", to: "/about" },
  { title: "Kontaktirajte nas", icon: "mdi-phone", to: "/contact" },
];

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
</script>

<template>
  <v-navigation-drawer
    width="300"
    location="left"
    sm="temporary"
    md="permanent"
  >
    <v-list color="blue-darken-2" nav>
      <v-list-item
        v-if="authStore.auth.isAuthenticated"
        lines="two"
        :title="profile.firstName + ' ' + profile.lastName"
        :subtitle="userStore.user.email"
      >
        <template v-slot:prepend>
          <ProfilePicture picture-size="50"/>
        </template>
      </v-list-item>
      <v-list-item
        v-for="item in navItems"
        :key="item.title"
        :prepend-icon="item.icon"
        :link="true"
        :to="item.to"
        exact
        :title="item.title"
      />
    </v-list>

    <template v-slot:append>
      <div class="pa-4">
        <RouterLink
          v-if="!authStore.auth.isAuthenticated"
          to="/login"
          class="no-underline"
        >
          <v-btn
            slim
            block
            append-icon="mdi-login"
            variant="outlined"
            color="blue-darken-2"
            text="Prijavi se"
          />
        </RouterLink>
        <v-btn
          v-else-if="authStore.auth.isAuthenticated"
          slim
          block
          append-icon="mdi-logout"
          @click="logOut"
          variant="flat"
          color="blue-darken-2"
          text="Odjavi se"
        />
      </div>
    </template>
  </v-navigation-drawer>
</template>

<style scoped>
.no-underline {
  text-decoration: none;
}
</style>
