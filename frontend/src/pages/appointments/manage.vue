<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useAppointmentStore } from "@/stores/useAppointmentStore";
import { useUserStore } from "@/stores/useUserStore";
import router from "@/router";
import BackButton from "@/components/BackButton.vue";
import {computed, onMounted, ref, watch} from "vue";

const appointments = ref([]);
const search = ref("");

const userStore = useUserStore();
const authStore = useAuthStore();
const appointmentStore = useAppointmentStore();

const formatDate = (date) => {
  return new Date(date).toLocaleDateString("hr-HR");
};

onMounted(async () => {
  await appointmentStore.getAppointments();
  appointments.value = appointmentStore.appointments;
});

watch(
    () => appointmentStore.appointments,
    (newAppointments) => {
      appointments.value = newAppointments;
    }
);

const filteredAppointments = computed(() => {
  if (!search.value) return appointments.value;
  return appointments.value.filter((appointment) => {
    const lowerCaseSearchTerm = search.value.toLowerCase();
    const date = formatDate(appointment.date);
    return appointment.patientName.toLowerCase().includes(lowerCaseSearchTerm) ||
        date.includes(lowerCaseSearchTerm) ||
        appointment.time.includes(lowerCaseSearchTerm) ||
        appointment.status.toLowerCase().includes(lowerCaseSearchTerm);
  });
})

if (!authStore.auth.isAuthenticated) router.push("/error/401");
else if (userStore.user.role !== "doctor") router.push("/error/403");
else if (!authStore.auth.hasProfile) router.push("/profile/create");
</script>

<template>
  <BackButton />
  <v-container>
    <v-row class="mx-2 d-flex align-center">
      <v-col>
        <h1 class="mb-4 my-4 font-weight-medium">
          Manage appointments
        </h1>
      </v-col>
      <v-col class="mb-4" cols="12" sm="12" md="4">
        <v-text-field
            v-model="search"
            prepend-inner-icon="mdi-magnify"
            label="Search"
            variant="outlined"
            density="compact"
            single-line
            hide-details
        />
      </v-col>
    </v-row>
    <v-row class="mx-0">
      <template
        v-for="appointment in filteredAppointments"
        :key="appointment.id"
      >
        <v-col cols="12" sm="6" md="3" lg="3" xl="2" v-if="appointment.id !== null">
          <v-card border elevation="0">
            <v-card-item>
              <v-card-title class="mb-6 mt-2 mx-2 wrap-text">
                <h4 class="font-weight-medium">Patients: </h4>
                <p class="font-weight-regular text-h5">{{ appointment.patientName }}</p>
              </v-card-title>
              <v-card-text class="mx-2" :class="$vuetify.display.md ? 'ml-0' : 'ml-4'">
                <v-row class="mb-2 d-flex justify-space-between">
                  <h4 class="font-weight-medium">Date:</h4>
                  <p :class="$vuetify.display.md ? 'ml-1' : 'ml-4'">{{ formatDate(appointment.date) }}</p>
                  <p></p>
                </v-row>
                <v-row class="mb-2 d-flex justify-space-between">
                  <h4 class="font-weight-medium">Time:</h4>
                  <p class="ml-3">{{ appointment.time }}</p>
                  <p></p>
                </v-row>
                <v-row class="mb-1 d-flex justify-space-between">
                  <h4 class="font-weight-medium">Status:</h4>
                  <p class="ml-5">{{ appointment.status }}</p>
                  <p></p>
                </v-row>
              </v-card-text>
              <v-card-actions
                v-if="appointment.status !== 'cancelled'"
                class="d-flex justify-center"
              >
                <v-btn
                  class="flex-fill"
                  color="blue-darken-2"
                  variant="tonal"
                  @click="appointmentStore.approveAppointment(appointment.id)"
                  >Approve</v-btn
                >
                <v-btn
                  class="flex-fill"
                  color="error"
                  variant="tonal"
                  @click="appointmentStore.rejectAppointment(appointment.id)"
                  >Reject</v-btn
                >
              </v-card-actions>
              <v-card-actions v-else class="d-flex justify-center">
                <v-btn disabled class="flex-fill" color="error" variant="tonal"
                  >Cancel</v-btn
                >
              </v-card-actions>
            </v-card-item>
          </v-card>
        </v-col>
      </template>
      <template v-if="appointments.length === 0">
        <v-card border elevation="0" class="py-11 my-4 flex-fill">
          <v-card-item>
            <v-card-title>
              <h4 class="font-weight-medium text-center text-medium-emphasis">
                No appointments found
              </h4>
            </v-card-title>
          </v-card-item>
        </v-card>
      </template>
    </v-row>

    <v-row class="mx-2 mt-4" justify="end">
      <RouterLink to="/appointments">
        <v-btn
          prepend-icon="mdi-calendar-clock"
          append-icon="mdi-arrow-right"
          variant="flat"
          elevation="0"
          text="All appointments"
          size="large"
          border
        />
      </RouterLink>
    </v-row>
  </v-container>
</template>

<style scoped>
.wrap-text {
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
}
</style>
