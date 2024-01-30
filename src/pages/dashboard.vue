<script setup>
  import PatientDashboard from "@/components/Patient/PatientDashboard.vue";
  import DoctorDashboard from "@/components/Doctor/DoctorDashboard.vue";
  import NotLoggedIn from "@/components/NotLoggedIn.vue";
  import {useAuthStore} from "@/stores/useAuthStore";

  const isPatient = localStorage.getItem("role") === "patient";
  const isDoctor = localStorage.getItem("role") === "doctor";
  const authStore = useAuthStore();
</script>

<template>
  <PatientDashboard v-if="isPatient"></PatientDashboard>
  <DoctorDashboard v-else-if="isDoctor"></DoctorDashboard>
  <div v-else-if="!authStore.isAuthenticated">
    <NotLoggedIn ></NotLoggedIn>
  </div>
  <div v-else>
    <h1>Greska pri učitavanju korisnika!</h1>
  </div>
</template>

<style scoped>

</style>