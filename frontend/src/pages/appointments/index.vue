<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useAppointmentStore } from "@/stores/useAppointmentStore";
import router from "@/router";
import { useUserStore } from "@/stores/useUserStore";

const authStore = useAuthStore();
const appointmentStore = useAppointmentStore();
const userStore = useUserStore();
const role = userStore.user.role;

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
}

if (!authStore.auth.hasProfile) {
  router.push("/doctor/create");
}

appointmentStore.getAppointments();

const patientHeaders = [
  { title: "ID", text: "ID", value: "id" },
  { title: "Doktor", text: "Doktor", value: "doctorName" },
  { title: "Datum", text: "Datum", value: "date" },
  { title: "Vrijeme", text: "Vrijeme", value: "time" },
  { title: "Status", text: "Status", value: "status" },
  { title: "Akcije", text: "Akcije", value: "actions", sortable: false , align: "center" },
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
  <v-container v-if="role === 'patient'">
    <v-btn
        @click="router.go(-1)"
        size="large"
        class="mt-2 mx-2">
      <v-icon>mdi-arrow-left</v-icon>
    </v-btn>
    <h1 class="mb-6 mt-4 mx-2 font-weight-medium">Moji naručeni termini</h1>
    <v-card class="mx-6" border elevation="0">
      <v-data-table
        :headers="patientHeaders"
        :items="appointmentStore.appointments"
        :items-per-page="10"
      >
        <template v-slot:item.date="{ item }">
          {{ item.date ? new Date(item.date).toLocaleDateString("hr-HR") : '' }}
        </template>
        <template v-slot:item.actions="{ item }">
          <v-btn
            v-if="item.id !== null && item.status === 'na čekanju'"
            prepend-icon="mdi-close"
            variant="tonal"
            color="error"
            width="100"
            @click="appointmentStore.cancelAppointment(item.id)"
          >
            Otkaži</v-btn
          >
          <v-btn
            v-else-if="item.id !== null && item.status === 'otkazan'"
            prepend-icon="mdi-check"
            variant="tonal"
            color="success"
            width="100"
            @click="appointmentStore.restoreAppointment(item.id)"
          >
            Vrati</v-btn
          >
        </template>
      </v-data-table>
    </v-card>
    <v-row class="mx-6 mt-4" justify="end">
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

  <v-container v-else-if="role === 'doctor'">
    <v-btn
        @click="router.go(-1)"
        size="large"
        class="mt-2 mx-2">
      <v-icon>mdi-arrow-left</v-icon>
    </v-btn>
    <h1 class="mb-6 mt-4 mx-2 font-weight-medium">Termini pacijenata</h1>
    <v-card class="mx-6" border elevation="0">
      <v-data-table
        :headers="doctorHeaders"
        :items="appointmentStore.appointments"
        :items-per-page="10"
      >
        <template v-slot:item.date="{ item }">
          {{ item.date ? new Date(item.date).toLocaleDateString("hr-HR") : '' }}
        </template>
      </v-data-table>
    </v-card>
    <v-row class="mx-6 mt-4" justify="end">
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
