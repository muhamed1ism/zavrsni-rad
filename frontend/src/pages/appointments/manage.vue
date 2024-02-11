<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useAppointmentStore } from "@/stores/useAppointmentStore";
import { useUserStore } from "@/stores/useUserStore";
import router from "@/router";

const userStore = useUserStore();
const authStore = useAuthStore();
const appointmentStore = useAppointmentStore();
const role = userStore.user.role;

const approve = async (id) => {
  try {
    await appointmentStore.approveAppointment(id);
  } catch (error) {
    console.log(error);
  }
};

const reject = async (id) => {
  try {
    await appointmentStore.rejectAppointment(id);
  } catch (error) {
    console.log(error);
  }
};

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
}

if (!authStore.auth.hasProfile) {
  router.push("/doctor/create");
}

if (role !== "doctor") {
  console.log("Nemate pristup ovoj stranici");
  router.push("/dashboard");
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString("hr-HR");
};

appointmentStore.getAppointments();
</script>

<template>
  <v-container>
    <h1 class="mt-4 mx-2 mb-6 font-weight-medium">Upravljenje narudžbama pacijenata</h1>
    <v-row class="mx-6">
      <template
        v-for="appointment in appointmentStore.appointments"
        :key="appointment.id"
      >
        <v-col sm="4" md="3" lg="3" v-if="appointment.id !== null">
          <v-card border elevation="0">
            <v-card-item>
              <v-card-title class="mb-6 mt-2 mx-2">
                <h4 class="font-weight-medium">
                  Pacijent: {{ appointment.patientName }}
                </h4>
              </v-card-title>
              <v-card-text class="mx-2">
                <v-row class="mb-2">
                  <h4 class="font-weight-medium">Datum:</h4>
                  <p class="ml-4">{{ formatDate(appointment.date) }}</p>
                </v-row>
                <v-row class="mb-2">
                  <h4 class="font-weight-medium">Vrijeme:</h4>
                  <p class="ml-3">{{ appointment.time }}</p>
                </v-row>
                <v-row class="mb-1">
                  <h4 class="font-weight-medium">Status:</h4>
                  <p class="ml-5">{{ appointment.status }}</p>
                </v-row>

              </v-card-text>
              <v-card-actions
                v-if="appointment.status !== 'otkazan'"
                class="d-flex justify-center"
              >
                <v-btn
                  class="flex-fill"
                  color="blue-darken-2"
                  variant="tonal"
                  @click="approve(appointment.id)"
                  >Odobri</v-btn
                >
                <v-btn
                  class="flex-fill"
                  color="error"
                  variant="tonal"
                  @click="reject(appointment.id)"
                  >Odbij</v-btn
                >
              </v-card-actions>
              <v-card-actions v-else class="d-flex justify-center">
                <v-btn disabled class="flex-fill" color="error" variant="tonal"
                  >Otkazan</v-btn
                >
              </v-card-actions>
            </v-card-item>
          </v-card>
        </v-col>
      </template>
    </v-row>
    <v-row class="mx-9 mt-4 d-flex justify-space-between">
      <RouterLink to="/appointments">
        <v-btn
            prepend-icon="mdi-calendar-clock"
            variant="flat"
            elevation="0"
            text="Naručeni termini"
            size="large"
            border
        />
      </RouterLink>

      <v-btn
          to="/patients"
          prepend-icon="mdi-account-multiple"
          variant="flat"
          elevation="0"
          text="Moji pacijenti"
          size="large"
          border
      />
    </v-row>
  </v-container>
</template>

<style scoped></style>
