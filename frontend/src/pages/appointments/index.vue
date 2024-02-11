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
  { title: "Akcije", text: "Akcije", value: "actions", sortable: false },
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
    <v-row class="mb-4 mt-2 mx-2">
      <h1>Moji termini pregleda</h1>
      <v-col class="d-flex justify-end">
        <v-btn
          to="/appointments/create"
          color="blue-darken-2"
          variant="tonal"

          >Novi termin
        </v-btn>
      </v-col>
    </v-row>

    <v-card border elevation="0">
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
  </v-container>

  <v-container v-else-if="role === 'doctor'">
    <h1 class="mb-4 mt-2 mx-2">Termini pacijenata</h1>
    <v-card border elevation="0">
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
  </v-container>
</template>

<style scoped></style>
