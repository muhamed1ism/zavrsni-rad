<script setup>
  import PatientDashboard from "@/components/Patient/PatientDashboard.vue";
  import DoctorDashboard from "@/components/Doctor/DoctorDashboard.vue";
  import NotLoggedIn from "@/components/NotLoggedIn.vue";
  import { useAuthStore } from "@/stores/useAuthStore";
  import { useUserStore } from "@/stores/useUserStore";
  import {usePatientStore} from "@/stores/usePatientStore";
  import {useDoctorStore} from "@/stores/useDoctorStore";

  const userStore = useUserStore();
  const authStore = useAuthStore();
  const role = userStore.user.role;
  if (role === "patient") {
    const patientStore = usePatientStore();
  }
  if (role === "doctor") {
    const doctorStore = useDoctorStore();
  }
</script>

<template>
  <PatientDashboard v-if="role === 'patient'"></PatientDashboard>
  <DoctorDashboard v-else-if="role === 'doctor'"></DoctorDashboard>
  <div v-else-if="!authStore.auth.isAuthenticated">
    <NotLoggedIn ></NotLoggedIn>
  </div>
  <div v-else>
    <h1>Greška pri učitavanju podataka korisnika!</h1>
  </div>
</template>

<style scoped>

</style>