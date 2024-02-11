<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useDoctorStore } from "@/stores/useDoctorStore";
import { useUserStore } from "@/stores/useUserStore";
import router from "@/router";

const authStore = useAuthStore();
const userStore = useUserStore();
const doctorStore = useDoctorStore();
const role = userStore.user.role;

doctorStore.getDoctors();

const doctorHeaders = [
  { title: "ID", value: "id", align: "start" },
  { title: "Ime", value: "name" },
  {
    title: "Specijalnost",
    value: "specialty",
  },
];

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
}

if (!authStore.auth.hasProfile) {
  router.push("/doctor/create");
}
</script>

<template>
  <v-container>
    <h1 class="mb-4 mt-2 mx-2">Doktori</h1>
    <v-card border elevation="0">
      <v-data-table
        :headers="doctorHeaders"
        :items="doctorStore.doctors"
        :items-per-page="10"
      />
    </v-card>
  </v-container>
</template>

<style scoped></style>
