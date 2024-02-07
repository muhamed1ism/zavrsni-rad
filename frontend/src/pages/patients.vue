<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { usePatientStore } from "@/stores/usePatientStore";
import { useUserStore } from "@/stores/useUserStore";
import router from "@/router";

const authStore = useAuthStore();
const patientStore = usePatientStore();
const userStore = useUserStore();
const role = userStore.user.role;

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
}

if (!authStore.auth.hasProfile) {
  router.push("/doctor/create");
}

if (role !== "doctor") {
  console.log("Nemate pristup ovoj stranici");
  router.push("/dashboard");
}

patientStore.getPatients();

const patientHeaders = [
  { title: "ID", text: "ID", value: "id", align: "start" },
  { title: "Ime", text: "Ime", value: "name" },
  { title: "Adresa", text: "Adresa", value: "address" },
  { title: "Datum rođenja", text: "Datum rođenja", value: "dateOfBirth" },
  { title: "Broj telefona", text: "Broj telefona", value: "phoneNumber" },
];
</script>

<template>
  <v-container>
    <h1 class="mb-4 mt-2 mx-2">Moji pacijenti</h1>
    <v-data-table
      :headers="patientHeaders"
      :items="patientStore.patients"
      :items-per-page="10"
    ></v-data-table>
  </v-container>
</template>

<style scoped></style>
