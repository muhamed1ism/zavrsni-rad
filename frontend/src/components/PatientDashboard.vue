<script setup>
import router from "@/router";
import { useAuthStore } from "@/stores/useAuthStore";
import { usePatientStore } from "@/stores/usePatientStore";
import { useAppointmentStore } from "@/stores/useAppointmentStore";

const authStore = useAuthStore();
const patientStore = usePatientStore();
const appointmentStore = useAppointmentStore();

appointmentStore.getApprovedAppointments();

const patient = patientStore.patient;

const buttons = [
  {
    title: "Moji podaci",
    icon: "mdi-account",
    to: "/patient",
  },
  {
    title: "Naručeni termini",
    icon: "mdi-calendar-clock",
    to: "/appointments",
  },
  {
    title: "Zakaži termin",
    icon: "mdi-calendar-plus",
    to: "/appointments/create",
  },
  {
    title: "Svi doktori",
    icon: "mdi-account-group",
    to: "/doctors",
  },
]

const patientHeaders = [
  { title: "ID", text: "ID", value: "id" },
  { title: "Doktor", text: "Doktor", value: "doctorName" },
  { title: "Datum", text: "Datum", value: "date" },
  { title: "Vrijeme", text: "Vrijeme", value: "time" },
];


if (!authStore.auth.isAuthenticated) {
  router.push("/login");
} else if (!authStore.auth.hasProfile) {
  router.push("/patient/create");
}
</script>

<template>
  <v-container>
      <h2 class="mx-2 mt-4 font-weight-regular">Dobro došli, </h2>
      <h1 class="mx-2 font-weight-medium"> {{ patient.firstName }} {{ patient.lastName }}</h1>

    <v-row class="ml-4 my-10 d-flex justify-center justify-space-around">
      <v-col v-for="button in buttons" :key="button.title">
        <v-btn
            :prepend-icon="button.icon" stacked
            :to="button.to"
            :text="button.title"
            size="x-large"
            width="350"
            variant="flat"
            elevation="0"
            border
            class="font-weight-regular"
        />
      </v-col>
    </v-row>

    <h2 class="mx-6 mb-4 font-weight-medium">Moji termini</h2>
    <v-card variant="flat" elevation="0" border class="mx-6">
      <v-data-table
          :headers="patientHeaders"
          :items="appointmentStore.appointments"
          :items-per-page="6"
      >
        <template v-slot:item.date="{ item }">
          {{ item.date ? new Date(item.date).toLocaleDateString("hr-HR") : '' }}
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<style scoped></style>
