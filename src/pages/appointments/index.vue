<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useAppointmentStore } from "@/stores/useAppointmentStore";
import router from "@/router";
import {useUserStore} from "@/stores/useUserStore";

const authStore = useAuthStore();
const appointmentStore = useAppointmentStore();
const userStore = useUserStore();
const role = userStore.user.role;

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
}

if (!authStore.auth.hasProfile) {
  router.push("/profile/create");
}

appointmentStore.getAppointments();

const patientHeaders = [
  { text: "ID", value: "id" },
  { text: "Doktor", value: "doctorName" },
  { text: "Datum", value: "date" },
  { text: "Vrijeme", value: "time" },
  { text: "Status", value: "status" },
];

const doctorHeaders = [
  {title: "ID", text: "ID", value: "id" },
  {title: "Pacijent", text: "Pacijent", value: "patientName" },
  {title: "Datum", text: "Datum", value: "date" },
  {title: "Vrijeme", text: "Vrijeme", value: "time" },
  {title: "Status", text: "Status", value: "status" },
  {title: "Akcije", text: "Akcije", value: "actions", sortable: false },
];
</script>

<template>
  <v-container v-if="role === 'patient'">
    <h1 class="mb-4 mt-2 mx-2">Moji termini</h1>
    <v-data-table
        :headers="patientHeaders"
        :items="appointmentStore.appointments"
        :items-per-page="10"
        class="elevation-1"
    ></v-data-table>
  </v-container>
  <v-container v-else-if="role === 'doctor'">
    <h1 class="mb-4 mt-2 mx-2">Termini pacijenata</h1>
    <v-data-table
        :headers="doctorHeaders"
        :items="appointmentStore.appointments"
        :items-per-page="10"
        class="elevation-1"
    >
      <template v-slot:item.actions="{ item }">
        <v-btn
            prepend-icon="mdi-close"
            variant="tonal"
            color="blue-darken-2"
            @click="appointmentStore.cancelAppointment(item.id)">
          Otkaži</v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>

<style scoped>

</style>