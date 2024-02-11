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
    <h1 class="mb-6 mt-4 mx-2 font-weight-medium">Doktori</h1>
    <v-card border elevation="0" class="mx-6">
      <v-data-table
        :headers="doctorHeaders"
        :items="doctorStore.doctors"
        :items-per-page="10"
      />
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
          v-if="role === 'doctor'"
          to="/patients"
          prepend-icon="mdi-account-group"
          variant="flat"
          elevation="0"
          text="Moji pacijenti"
          size="large"
          border
      />
      <v-btn
          v-if="role === 'patient'"
          to="/appointments"
          prepend-icon="mdi-calendar-clock"
          variant="flat"
          elevation="0"
          text="Moji termini"
          size="large"
          border
      />
    </v-row>
  </v-container>
</template>

<style scoped></style>
