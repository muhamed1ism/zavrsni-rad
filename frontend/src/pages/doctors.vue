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
} else if (!authStore.auth.hasProfile) {
  router.push("/dashboard")
}
</script>

<template>
  <v-container>
    <v-btn
        @click="router.go(-1)"
        size="large"
        class="mt-2 mx-2">
      <v-icon>mdi-arrow-left</v-icon>
    </v-btn>
    <h1 class="mb-6 mt-4 mx-2 font-weight-medium">Doktori</h1>
    <v-card border elevation="0" class="mx-6">
      <v-data-table
        :headers="doctorHeaders"
        :items="doctorStore.doctors"
        :items-per-page="10"
      >
        <template v-slot:no-data>
          <p>Nema doktora</p>
        </template>
      </v-data-table>
    </v-card>
    <v-row class="mx-6 mt-4" justify="end">
      <v-btn
          v-if="role === 'doctor'"
          to="/patients"
          prepend-icon="mdi-account-group"
          append-icon="mdi-arrow-right"
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
          append-icon="mdi-arrow-right"
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
