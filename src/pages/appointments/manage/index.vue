<script setup>
  import { useAuthStore } from "@/stores/useAuthStore";
  import { useAppointmentStore } from "@/stores/useAppointmentStore";
  import {useUserStore} from "@/stores/useUserStore";
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

  appointmentStore.getAppointments();
</script>

<template>

  <v-container>
    <h1 class="my-4">Upravljenje narudžbama pacijenata</h1>
    <v-row>
      <template v-for="appointment in appointmentStore.appointments"
                :key="appointment.id">
        <v-col sm="4" md="3" lg="3"
               v-if="appointment.id !== null">
          <v-card
              border
              variant="tonal">
            <v-card-item>
              <v-card-title>
                <h2 class="text-high-emphasis mb-4 mt-2 mx-2">
                  Pacijent: {{appointment.patientName}}</h2>
              </v-card-title>
              <v-card-text>
                <p>Datum: {{appointment.date}}</p>
                <p>Vrijeme: {{appointment.time}}</p>
                <p>Status: {{appointment.status}}</p>
              </v-card-text>
              <v-card-actions v-if="appointment.status !== 'otkazan'" class="d-flex justify-center">
                <v-btn
                    class="flex-fill"
                    color="blue-darken-2"
                    variant="tonal"
                    @click="approve(appointment.id)">Odobri</v-btn>
                <v-btn
                    class="flex-fill"
                    color="error"
                    variant="tonal"
                    @click="reject(appointment.id)">Odbij</v-btn>
              </v-card-actions>
              <v-card-actions v-else class="d-flex justify-center">
                <v-btn
                    disabled
                    class="flex-fill"
                    color="error"
                    variant="tonal">Otkazan</v-btn>
              </v-card-actions>
            </v-card-item>
          </v-card>
        </v-col>
      </template>

    </v-row>
  </v-container>


</template>

<style scoped>

</style>