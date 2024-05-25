<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useAppointmentStore } from "@/stores/useAppointmentStore";
import router from "@/router";
import { useUserStore } from "@/stores/useUserStore";
import BackButton from "@/components/BackButton.vue";

const { auth } = useAuthStore();
const { appointments, getAppointments, cancelAppointment, restoreAppointment } = useAppointmentStore();
const { user } = useUserStore();

if (!auth.isAuthenticated) router.push("/error/401");
else if (!auth.hasProfile) router.push("/profile/create");

getAppointments();

const patientHeaders = [
  { title: "ID", text: "ID", value: "id" },
  { title: "Doktor", text: "Doktor", value: "doctorName" },
  { title: "Datum", text: "Datum", value: "date" },
  { title: "Vrijeme", text: "Vrijeme", value: "time" },
  { title: "Status", text: "Status", value: "status" },
  {
    title: "Akcije",
    text: "Akcije",
    value: "actions",
    sortable: false,
    align: "center",
  },
];

const doctorHeaders = [
  { title: "ID", text: "ID", value: "id" },
  { title: "Pacijent", text: "Pacijent", value: "patientName" },
  { title: "Datum", text: "Datum", value: "date" },
  { title: "Vrijeme", text: "Vrijeme", value: "time" },
  { title: "Status", text: "Status", value: "status" },
];
</script>

<template>
  <BackButton />
  <v-container v-if="user.role === 'patient'">
    <h1 class="mb-4 my-4 mx-2 font-weight-medium">Moji naručeni termini</h1>
    <v-card border elevation="0">
      <v-data-table
        :headers="patientHeaders"
        :items="appointments"
        items-per-page-text="Broj stavki po stranici"
        :items-per-page="10"
      >
        <template v-slot:item.date="{ item }">
          {{ item.date ? new Date(item.date).toLocaleDateString("hr-HR") : "" }}
        </template>
        <template v-slot:no-data>
          <p>Nema naručenih termina</p>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-btn
            v-if="item.id !== null && item.status === 'na čekanju'"
            prepend-icon="mdi-close"
            variant="tonal"
            color="error"
            width="100"
            @click="cancelAppointment(item.id)"
          >
            Otkaži</v-btn
          >
          <v-btn
            v-else-if="item.id !== null && item.status === 'otkazan'"
            prepend-icon="mdi-check"
            variant="tonal"
            color="success"
            width="100"
            @click="restoreAppointment(item.id)"
          >
            Vrati</v-btn
          >
        </template>
      </v-data-table>
    </v-card>
    <v-row class="mx-2 mt-4" justify="end">
      <v-btn
        to="/appointments/create"
        prepend-icon="mdi-calendar-plus"
        append-icon="mdi-arrow-right"
        variant="flat"
        elevation="0"
        text="Zakaži termin"
        size="large"
        border
      />
    </v-row>
  </v-container>

  <v-container v-else-if="user.role === 'doctor'">
    <h1 class="mb-4 my-4 mx-2 font-weight-medium">Termini pacijenata</h1>
    <v-card border elevation="0">
      <v-data-table
        :headers="doctorHeaders"
        :items="appointments"
        items-per-page-text="Broj stavki po stranici"
        :items-per-page="10"
      >
        <template v-slot:item.date="{ item }">
          {{ item.date ? new Date(item.date).toLocaleDateString("hr-HR") : "" }}
        </template>
        <template v-slot:no-data>
          <p>Nema naručenih termina</p>
        </template>
      </v-data-table>
    </v-card>
    <v-row class="mx-2 mt-4" justify="end">
      <v-btn
        to="/appointments/manage"
        prepend-icon="mdi-calendar-edit"
        append-icon="mdi-arrow-right"
        variant="flat"
        elevation="0"
        text="Upravljanje terminima"
        size="large"
        border
      />
    </v-row>
  </v-container>
</template>

<style scoped></style>
