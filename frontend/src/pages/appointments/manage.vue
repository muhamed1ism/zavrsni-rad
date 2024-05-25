<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useAppointmentStore } from "@/stores/useAppointmentStore";
import { useUserStore } from "@/stores/useUserStore";
import router from "@/router";
import BackButton from "@/components/BackButton.vue";

const { user } = useUserStore();
const { auth } = useAuthStore();
const { appointments, approveAppointment, rejectAppointment, getAppointments } = useAppointmentStore();

const approve = async (id) => {
  try {
    await approveAppointment(id);
  } catch (error) {
    console.log(error);
  }
};

const reject = async (id) => {
  try {
    await rejectAppointment(id);
  } catch (error) {
    console.log(error);
  }
};

const formatDate = (date) => {
  return new Date(date).toLocaleDateString("hr-HR");
};

getAppointments();

if (!auth.isAuthenticated) router.push("/error/401");
else if (user.role !== "doctor") router.push("/error/403");
else if (!auth.hasProfile) router.push("/profile/create");
</script>

<template>
  <BackButton />
  <v-container>
    <h1 class="mb-4 my-4 mx-2 font-weight-medium">
      Upravljenje narudžbama pacijenata
    </h1>
    <v-row class="mx-0">
      <template
        v-for="appointment in appointments"
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
      <template v-if="appointments.length === 0">
        <v-card border elevation="0" class="py-11 my-4 flex-fill">
          <v-card-item>
            <v-card-title>
              <h4 class="font-weight-medium text-center text-medium-emphasis">
                Nema naručenih termina
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
          text="Naručeni termini"
          size="large"
          border
        />
      </RouterLink>
    </v-row>
  </v-container>
</template>

<style scoped></style>
