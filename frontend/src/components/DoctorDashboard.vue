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
    title: "Odobrene narudžbe",
    style: "background-color: mediumseagreen",
    icon: "mdi-check",
    value: appointmentStore.approvedAppointments,
  },
  {
    title: "Narudžbe na čekanju",
    style: "background-color: darkgray",
    icon: "mdi-clock",
    value: appointmentStore.pendingAppointments,
  },
  {
    title: "Odbijene narudžbe",
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

if (!authStore.auth.hasProfile) {
  router.push("/doctor/create");
}
</script>

<template>
  <v-container>
    <h1 class="mb-4 mt-2 mx-2">Nadzorna ploča doktora</h1>
    <v-row>
      <v-col cols="12" sm="6" lg="4" v-for="card in cardHeaders" :key="card.title">
        <v-card border elevation="0">
          <v-row class="py-3">
            <v-col cols="4" class="d-flex justify-center align-center" :style="card.style">
              <v-icon color="white">{{ card.icon }}</v-icon>
            </v-col>
            <v-col class="text-center">
              <v-card-title>{{ card.title }}</v-card-title>
              <v-card-item>{{ card.value }}</v-card-item>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="6" lg="6">
        <h1>Pacijenti</h1>
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
      <v-col>
        <h1>Narudžbe</h1>
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
  </v-container>
</template>

<style scoped></style>
