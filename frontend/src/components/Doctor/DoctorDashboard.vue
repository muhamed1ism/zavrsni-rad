<script setup>
import { usePatientStore } from "@/stores/usePatientStore";
import { useDoctorStore } from "@/stores/useDoctorStore";
import { useAppointmentStore } from "@/stores/useAppointmentStore";
import {computed, onMounted, ref, watch} from "vue";

const patients = ref([]);
const appointments = ref([]);

const patientStore = usePatientStore();
const doctorStore = useDoctorStore();
const appointmentStore = useAppointmentStore();

onMounted(async () => {
  await patientStore.getPatients();
  await doctorStore.getDoctor();
  await appointmentStore.getAppointments();
  await appointmentStore.getApprovedAppointments();
  await appointmentStore.countApprovedAppointments();
  await appointmentStore.countPendingAppointments();
  await appointmentStore.countRejectedAppointments();
  patients.value = patientStore.patients;
  appointments.value = appointmentStore.appointments;
});

watch(
    [() => patientStore.patients, () => appointmentStore.appointments],
    ([newPatients, newAppointments]) => {
      patients.value = newPatients;
      appointments.value = newAppointments;
    }
);

const cardHeaders = computed(() => [
  {
    title: "Odobreni",
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
    title: "Odbijeni",
    style: "background-color: indianred",
    icon: "mdi-close",
    value: appointmentStore.rejectedAppointments,
  },
]);

const patientHeaders = [
  { title: "ID", value: "id", align: "start" },
  { title: "Ime", value: "name" },
  { title: "Datum rođenja", value: "dateOfBirth" },
  { title: "Broj telefona", value: "phoneNumber" },
];

const appointmentHeaders = [
  { title: "ID", value: "id", align: "start" },
  { title: "Pacijent", value: "patientName" },
  { title: "Datum narudžbe", value: "date" },
  { title: "Vrijeme narudžbe", value: "time" },
];

const buttons = [
  {
    title: "Svi naručeni termini",
    icon: "mdi-calendar-clock",
    to: "/appointments",
  },
  {
    title: "Upravljanje terminima",
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
  },
];
</script>

<template>
  <v-container>
    <h1
      class="mb-4 my-4 mx-2 font-weight-medium"
      :class="$vuetify.display.xs ? 'text-center' : ''"
    >
      Nadzorna ploča doktora
    </h1>
    <h2 class="mx-6 mb-4 font-weight-regular">Broj naručenih termina</h2>
    <v-row class="mx-4">
      <v-col
        cols="12"
        sm="4"
        md="4"
        lg="4"
        v-for="card in cardHeaders"
        :key="card.title"
      >
        <v-card border elevation="0">
          <v-row>
            <v-col
              cols="3"
              sm="12"
              md="4"
              class="d-flex justify-center align-center py-12"
              :style="card.style"
            >
              <v-icon color="white">{{ card.icon }}</v-icon>
            </v-col>
            <v-col cols="9" sm="12" md="8" class="text-center">
              <v-card-title>{{ card.title }}</v-card-title>
              <v-card-item>{{ card.value }}</v-card-item>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mx-4">
      <v-col cols="12" md="6">
        <RouterLink class="no-decoration" to="patients">
          <h2 class="mb-4 font-weight-regular">Pacijenti</h2>
        </RouterLink>
        <v-card border elevation="0">
          <v-data-table
            :headers="patientHeaders"
            :items="patients"
            hide-default-footer
            items-per-page-text="Broj stavki po stranici"
            :items-per-page="5"
          >
            <template v-slot:item.dateOfBirth="{ item }">
              {{
                item.dateOfBirth
                  ? new Date(item.dateOfBirth).toLocaleDateString("hr-HR")
                  : ""
              }}
            </template>
            <template v-slot:no-data>
              <p>Nema naručenih pacijenata</p>
            </template>
          </v-data-table>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <RouterLink class="no-decoration" to="appointments">
          <h2 class="mb-4 font-weight-regular">Odobreni naručeni termini</h2>
        </RouterLink>
        <v-card border elevation="0">
          <v-data-table
            :headers="appointmentHeaders"
            :items="appointments"
            hide-default-footer
            items-per-page-text="Broj stavki po stranici"
            :items-per-page="5"
          >
            <template v-slot:item.date="{ item }">
              {{
                item.date ? new Date(item.date).toLocaleDateString("hr-HR") : ""
              }}
            </template>
            <template v-slot:no-data>
              <p>Nema naručenih termina</p>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="ma-4 mt-12">
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
  </v-container>
</template>

<style scoped>
.no-decoration {
  text-decoration: none;
  color: unset;
}
</style>
