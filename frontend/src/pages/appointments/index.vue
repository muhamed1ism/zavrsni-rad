<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useAppointmentStore } from "@/stores/useAppointmentStore";
import router from "@/router";
import { useUserStore } from "@/stores/useUserStore";
import BackButton from "@/components/BackButton.vue";
import {onMounted, ref, watch} from "vue";
import PatientAppointments from "@/components/Patient/PatientAppointments.vue";
import DoctorAppointments from "@/components/Doctor/DoctorAppointments.vue";

const appointments = ref([]);

const authStore = useAuthStore();
const appointmentStore = useAppointmentStore();
const userStore = useUserStore();

onMounted(
  async () => {
    await appointmentStore.getAppointments();
    appointments.value = appointmentStore.appointments;
  }
);

watch(
  () => appointmentStore.appointments,
  (newAppointments) => {
    appointments.value = newAppointments;
  }
);

if (!authStore.auth.isAuthenticated) router.push("/error/401");
else if (!authStore.auth.hasProfile) router.push("/profile/create");
</script>

<template>
  <BackButton />
  <PatientAppointments v-if="userStore.user.role === 'patient'" :appointments="appointments"
                       :appointment-store="appointmentStore"/>
  <DoctorAppointments v-else-if="userStore.user.role === 'doctor'" :appointments="appointments"/>
</template>

<style scoped></style>
