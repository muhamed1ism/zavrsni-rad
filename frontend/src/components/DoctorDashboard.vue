<script setup>
import router from "@/router";
import { useAuthStore } from "@/stores/useAuthStore";
import { usePatientStore } from "@/stores/usePatientStore";
import { useAppointmentStore } from "@/stores/useAppointmentStore";
import {computed} from "vue";

const authStore = useAuthStore();
const patientStore = usePatientStore();
const appointmentStore = useAppointmentStore();

appointmentStore.countApprovedAppointments();
appointmentStore.countPendingAppointments();
appointmentStore.countRejectedAppointments();
patientStore.getPatients();
appointmentStore.getApprovedAppointments();


const cardHeaders = computed(() => [
  {
    title: "Odobren",
    style: "background-color: mediumseagreen",
    icon: "mdi-check",
    value: appointmentStore.approvedAppointments,
  },
  {
    title: "Na čekanju",
    style: "background-color: darkgray",
    icon: "mdi-clock",
    value: appointmentStore.pendingAppointments,
  },
  {
    title: "Odbijen",
    style: "background-color: indianred",
    icon: "mdi-close",
    value: appointmentStore.rejectedAppointments,
  }
])

const patientHeaders = [
  { title: "ID", value: "id", align: "start" },
  { title: "Ime", value: "name" },
  { title: "Datum rođenja", value: "dateOfBirth" },
  { title: "Broj telefona", value: "phoneNumber"},
]

const appointmentHeaders = [
  { title: "ID", value: "id", align: "start" },
  { title: "Pacijent", value: "patientName" },
  { title: "Datum narudžbe", value: "date" },
  { title: "Vrijeme narudžbe", value: "time"},
]

const buttons = [
  {
    title: "Naručeni termini",
    icon: "mdi-calendar-clock",
    to: "/appointments",
  },
  {
    title: "Upravljanje narudžbama",
    icon: "mdi-calendar-edit",
    to: "/appointments/manage",
  },
  {
    title: "Moji pacijenti",
    icon: "mdi-account-multiple",
    to: "/patients",
  },
  {
    title: "Svi doktori",
    icon: "mdi-account-group",
    to: "/doctors",
  }
]

if (!authStore.auth.hasProfile) {
  router.push("/doctor/create");
}
</script>

<template>
  <v-container>
    <h1 class="mb-6 mt-4 mx-2 font-weight-medium">Nadzorna ploča doktora</h1>
    <h2 class="mx-6 mb-4 font-weight-regular">Broj naručenih termina</h2>
    <v-row class="mx-4">
      <v-col cols="12" sm="6" md="4" lg="4" v-for="card in cardHeaders" :key="card.title">
        <v-card border elevation="0">
          <v-row>
            <v-col cols="3" md="4" class="d-flex justify-center align-center" :style="card.style">
              <v-icon color="white">{{ card.icon }}</v-icon>
            </v-col>
            <v-col cols="9" md="8" class="text-center">
              <v-card-title>{{ card.title }}</v-card-title>
              <v-card-item>{{ card.value }}</v-card-item>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mx-4">
      <v-col cols="12" sm="6">
        <h2 class="mb-4 font-weight-regular">Pacijenti</h2>
        <v-card
          border elevation="0">
          <v-data-table
              :headers="patientHeaders"
              :items="patientStore.patients"
              :items-per-page="5">
            <template v-slot:item.dateOfBirth="{ item }">
              {{ item.dateOfBirth ? new Date(item.dateOfBirth).toLocaleDateString("hr-HR") : '' }}
            </template>
          </v-data-table>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6">
        <h2 class="mb-4 font-weight-regular">Naručeni termini</h2>
        <v-card
          border elevation="0">
          <v-data-table
              :headers="appointmentHeaders"
              :items="appointmentStore.appointments"
              :items-per-page="5">
            <template v-slot:item.date="{ item }">
              {{ item.date ? new Date(item.date).toLocaleDateString("hr-HR") : '' }}
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mx-6 mt-12 d-flex justify-center justify-space-around">
      <v-col class="v-col-auto" v-for="button in buttons" :key="button.title">
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
        >
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped></style>
