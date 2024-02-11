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
  { title: "ID", value: "id", align: "start" },
  { title: "Ime", value: "name" },
  { title: "Adresa", value: "address" },
  { title: "Datum rođenja", value: "dateOfBirth" },
  { title: "Broj telefona", value: "phoneNumber" },
];
</script>

<template>
  <v-container>
    <h1 class="mb-6 mt-4 mx-2 font-weight-medium">Moji pacijenti</h1>
    <v-card border elevation="0" class="mx-6">
      <v-data-table
        :headers="patientHeaders"
        :items="patientStore.patients"
        :items-per-page="10"
      >
        <template v-slot:item.dateOfBirth="{ item }">
          {{ item.dateOfBirth ? new Date(item.dateOfBirth).toLocaleDateString("hr-HR") : '' }}
        </template>
      </v-data-table>
    </v-card>
    <v-row class="mx-6 mt-4 d-flex justify-space-between">
      <v-btn
          to="/dashboard"
          prepend-icon="mdi-arrow-left"
          variant="flat"
          elevation="0"
          text="Nazad na početnu"
          size="large"
          border
      />
      <v-btn
          to="/doctors"
          prepend-icon="mdi-account-group"
          variant="flat"
          elevation="0"
          text="Svi doktori"
          size="large"
          border
      />
    </v-row>
  </v-container>
</template>

<style scoped></style>
