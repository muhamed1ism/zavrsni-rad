<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useDoctorStore } from "@/stores/useDoctorStore";
import { useUserStore } from "@/stores/useUserStore";
import router from "@/router";

const authStore = useAuthStore();
const doctorStore = useDoctorStore();
const userStore = useUserStore();
const role = userStore.user.role;

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
}

if (!authStore.auth.hasProfile) {
  router.push("/doctor/create");
}

doctorStore.getDoctors();

const doctors = [
  { title: "ID", text: "ID", value: "id", align: "start" },
  { title: "Ime", text: "Ime", value: "name", align: "center" },
  {
    title: "Specijalnost",
    text: "Specijalnost",
    value: "specialty",
    align: "end",
  },
];
</script>

<template>
  <v-container>
    <h1 class="mb-4 mt-2 mx-2">Doktori</h1>
    <v-data-table
      :headers="doctors"
      :items="doctorStore.doctors"
      :items-per-page="10"/>
  </v-container>
</template>

<style scoped></style>
