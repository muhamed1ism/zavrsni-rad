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
} else if (!authStore.auth.hasProfile) {
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
    <v-btn
        @click="router.go(-1)"
        size="large"
        class="mt-2 mx-2">
      <v-icon>mdi-arrow-left</v-icon>
    </v-btn>
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
        <template v-slot:no-data>
          <p>Nema naručenih pacijenata</p>
        </template>
      </v-data-table>
    </v-card>
    <v-row class="mx-6 mt-4" justify="end">
      <v-btn
          to="/doctors"
          prepend-icon="mdi-account-group"
          append-icon="mdi-arrow-right"
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
