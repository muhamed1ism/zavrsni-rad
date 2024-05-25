<script setup>
import { usePatientStore } from "@/stores/usePatientStore";
import { useAppointmentStore } from "@/stores/useAppointmentStore";
import ProfilePicture from "@/components/ProfilePicture.vue";

const { patient, getPatient } = usePatientStore();
const { appointments, getApprovedAppointments } = useAppointmentStore();

getApprovedAppointments();
getPatient();

const buttons = [
  {
    title: "Moj profil",
    icon: "mdi-account",
    to: "/profile",
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
];

const patientHeaders = [
  { title: "ID", text: "ID", value: "id" },
  { title: "Doktor", text: "Doktor", value: "doctorName" },
  { title: "Datum", text: "Datum", value: "date" },
  { title: "Vrijeme", text: "Vrijeme", value: "time" },
];
</script>

<template>
  <v-container fluid>
    <v-row class="mt-2 mx-2">
      <v-col
        cols="auto"
        :class="
          $vuetify.display.xs
            ? 'v-col-12 d-flex justify-center align-center'
            : ''
        "
      >
        <ProfilePicture picture-size="120"/>
      </v-col>
      <v-col cols="auto" :class="$vuetify.display.xs ? 'v-col-12' : ''">
        <h2
          :class="
            $vuetify.display.xs
              ? 'text-sm-welcome text-center'
              : 'mx-2 mt-4 font-weight-regular'
          "
        >
          Dobro došli,
        </h2>
        <h1
          :class="
            $vuetify.display.xs
              ? 'text-sm-name text-center'
              : 'mx-2 font-weight-medium'
          "
        >
          {{ patient.firstName }} {{ patient.lastName }}
        </h1>
      </v-col>
    </v-row>

    <v-row class="ma-4 my-8">
      <v-col
        v-for="button in buttons"
        :key="button.title"
        md="3"
        sm="6"
        xs="12"
      >
        <v-btn
          :prepend-icon="button.icon"
          stacked
          :to="button.to"
          :text="button.title"
          size="x-large"
          width="48rem"
          variant="flat"
          elevation="0"
          border
          class="font-weight-regular text-center"
        />
      </v-col>
    </v-row>

    <h2 class="mx-6 mb-4 font-weight-medium">Moji termini</h2>
    <v-card variant="flat" elevation="0" border class="mx-6">
      <v-data-table
        :headers="patientHeaders"
        :items="appointments"
        items-per-page-text="Broj stavki po stranici"
        :items-per-page="6"
      >
        <template v-slot:item.date="{ item }">
          {{ item.date ? new Date(item.date).toLocaleDateString("hr-HR") : "" }}
        </template>
        <template v-slot:no-data>
          <p>Nema zakazanih termina</p>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<style scoped>
.text-sm-welcome {
  font-size: 1.1rem;
}
.text-sm-name {
  font-size: 1.6rem;
}
</style>
