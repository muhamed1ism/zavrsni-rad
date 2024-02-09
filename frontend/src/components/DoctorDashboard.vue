<script setup>
import router from "@/router";
import { useAuthStore } from "@/stores/useAuthStore";
import { usePatientStore } from "@/stores/usePatientStore";
import { useAppointmentStore } from "@/stores/useAppointmentStore";

const authStore = useAuthStore();
const patientStore = usePatientStore();
const appointmentStore = useAppointmentStore();

const cards = [
  {
    title: "Odobrene narudžbe",
    style: "background-color: mediumseagreen",
    icon: "mdi-check",
    value: 0,
  },
  {
    title: "Narudžbe na čekanju",
    style: "background-color: darkgray",
    icon: "mdi-clock",
    value: 0,
  },
  {
    title: "Odbijene narudžbe",
    style: "background-color: indianred",
    icon: "mdi-close",
    value: 0,
  }
]

const patients = [
  { title: "ID", text: "ID", value: "id", align: "start" },
  { title: "Ime", text: "Ime", value: "name" },
  { title: "Datum rođenja", text: "Datum rođenja", value: "dateOfBirth" },
  { title: "Broj telefona", text: "Broj telefona", value: "phoneNumber", align: "end" },
]

const appointments = [
  { title: "ID", text: "ID", value: "id", align: "start" },
  { title: "Pacijent", text: "Pacijent", value: "patientName" },
  { title: "Datum narudžbe", text: "Datum narudžbe", value: "date" },
  { title: "Vrijeme narudžbe", text: "Vrijeme narudžbe", value: "time", align: "end" },
]

if (!authStore.auth.hasProfile) {
  router.push("/doctor/create");
}
</script>

<template>
  <v-container>
    <h1 class="mb-4 mt-2 mx-2">Nadzorna ploča doktora</h1>
    <v-row>
      <v-col cols="12" sm="6" lg="4" v-for="card in cards" :key="cards">
        <v-card>
          <v-row class="py-3">
            <v-col cols="4" class="d-flex justify-center align-center" :style="card.style">
              <v-icon>{{ card.icon }}</v-icon>
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
        <v-data-table
            :headers="patients"
            :items="patientStore.patients"
            :items-per-page="5"/>
      </v-col>
      <v-col>
        <h1>Narudžbe</h1>
        <v-data-table
            :headers="appointments"
            :items="appointmentStore.appointments"
            :items-per-page="5"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped></style>
