<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useDoctorStore } from "@/stores/useDoctorStore";
import { useUserStore } from "@/stores/useUserStore";
import router from "@/router";
import BackButton from "@/components/BackButton.vue";

const { auth } = useAuthStore();
const { user } = useUserStore();
const { doctors, getDoctors } = useDoctorStore();

getDoctors();

const doctorHeaders = [
  { title: "ID", value: "id", align: "start" },
  { title: "Ime", value: "name" },
  {
    title: "Specijalnost",
    value: "specialty",
  },
];

if (!auth.isAuthenticated) router.push("/error/401");
else if (!auth.hasProfile) router.push("/profile/create");
</script>

<template>
  <BackButton />
  <v-container>
    <h1 class="mb-4 my-4 mx-2 font-weight-medium">Doktori</h1>
    <v-card border elevation="0">
      <v-data-table
        :headers="doctorHeaders"
        :items="doctors"
        items-per-page-text="Broj stavki po stranici"
        :items-per-page="10"
      >
        <template v-slot:no-data>
          <p>Nema doktora</p>
        </template>
      </v-data-table>
    </v-card>
    <v-row class="mx-2 mt-4" justify="end">
      <v-btn
        v-if="user.role === 'doctor'"
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
        v-if="user.role === 'patient'"
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
